#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

# Import the original script functions
from aicodemerge import parse_arguments, custom_config, parse_gitignore, should_include_file, list_directory, get_file_extension, append_file_content

class DropZone(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Project Folder Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
                border-radius: 10px;
                font-size: 20px;
            }
        ''')
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.parent().process_folder(files[0])

class AICodeMergeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.dropzone = DropZone()
        layout.addWidget(self.dropzone)

        self.select_button = QPushButton('Select Folder')
        self.select_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle('AICodeMerge GUI')
        self.setGeometry(300, 300, 400, 300)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.process_folder(folder)

    def process_folder(self, folder_path):
        if not os.access(folder_path, os.R_OK):
            QMessageBox.critical(self, "Permission Denied", f"Cannot access the folder: {folder_path}\nPlease check your permissions and try again.")
            return

        args = parse_arguments()
        args.project_path = folder_path
        args.verbose = True  # Enable verbose output for GUI

        try:
            max_depth, max_size, patterns, exclude_patterns = custom_config()
        except Exception as e:
            QMessageBox.critical(self, "Configuration Error", f"Error in custom configuration: {str(e)}")
            return

        self.progress_bar.setValue(0)

        try:
            self.run_aicodemerge(args, max_depth, max_size, patterns, exclude_patterns)
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Process Complete", "AICodeMerge has finished processing the folder.")
        except Exception as e:
            QMessageBox.critical(self, "Processing Error", f"An error occurred while processing: {str(e)}")

    def run_aicodemerge(self, args, max_depth, max_size, patterns, exclude_patterns):
        project_name = os.path.basename(os.path.abspath(args.project_path))
        output_file = f"{project_name}_output.md"
        
        gitignore_matcher = parse_gitignore(os.path.join(args.project_path, '.gitignore'), exclude_patterns)
        
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("# Project Knowledge for AI Analysis\n\n")
            # ... (write other initial content)

        files_to_process = []
        for root, _, files in os.walk(args.project_path):
            if 'node_modules' in root.split(os.path.sep):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                if should_include_file(file_path, gitignore_matcher, patterns):
                    files_to_process.append(file_path)

        total_files = len(files_to_process)
        for i, file_path in enumerate(files_to_process, 1):
            try:
                append_file_content(file_path, output_file, max_size)
            except PermissionError:
                print(f"Permission denied: Unable to read {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
            self.progress_bar.setValue(int((i / total_files) * 100))

        print(f"Markdown file created: {output_file}")
        print(f"Location: {os.path.abspath(output_file)}")

def main():
    app = QApplication(sys.argv)
    ex = AICodeMergeGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
