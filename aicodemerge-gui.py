#!/usr/bin/env python3

import sys
import datetime
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox, QLineEdit, QSpinBox, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

# Import only necessary functions from the original script
from aicodemerge import parse_gitignore, should_include_file, append_file_content

DEFAULT_EXCLUDE_PATTERNS = [
    # Git-related
    '.git',  # Exclude the entire .git directory
    '.git/*',  # Exclude all direct children of .git
    '**/.git',  # Exclude .git directories at any depth
    '**/.git/**',  # Exclude all contents of any .git directory at any depth

    # Version Control Systems
    '.svn', '.hg', '.gitignore', '.gitattributes',

    # Dependency Directories
    'node_modules', 'node_modules/**', 'vendor', 'bower_components', 'jspm_packages',

    # Build Outputs
    'build', 'dist', 'out', 'target', '.next/**', 'out/**',

    # Compiled Files
    '*.pyc', '*.pyo', '*.mo', '*.class', '*.dll', '*.exe', '*.o', '*.obj', '*.so',
    '*.dylib', '*.ncb', '*.sdf', '*.suo', '*.pdb', '*.idb', '.com', '*.exe', '*.o',
    '*.bundle.js', '*.chunk.js',

    # Logs and Databases
    '*.log', '*.sql', '*.sqlite', '*.sqlite3', '*.sqlite3-journal',

    # OS Generated Files
    '.DS_Store', 'Thumbs.db', 'desktop.ini', '._*', '.Spotlight-V100', '.Trashes',
    'ehthumbs.db', 'ehthumbs_vista.db',

    # Package Manager Files
    'package-lock.json', 'yarn.lock', 'composer.lock', 'Gemfile.lock',

    # Cache and Temporary Files
    '.cache', '.tmp', '.temp', '.sass-cache', '__pycache__', '*.py[cod]',
    '.eslintcache', '.stylelintcache', '.phpunit.result.cache',

    # IDE and Editor Files
    '.vscode', '.idea', '*.swp', '*.swo', '*.sublime-*', '*.code-workspace',
    '.project', '.classpath', '.settings/', '*.launch', '.history/',

    # Test and Coverage
    'coverage', '.nyc_output', '.pytest_cache', '.tox', '.nox',
    'nosetests.xml', 'coverage.xml',

    # Documentation
    'docs', '*.md', '*.rst', '*.txt',

    # Media and Archives
    '*.jpg', '*.jpeg', '*.png', '*.gif', '*.ico', '*.mov', '*.mp4', '*.mp3',
    '*.flv', '*.fla', '*.zip', '*.tar.gz', '*.rar',

    # Configuration and Environment Files
    '.env', '.env.*', 'config.json', 'settings.json',

    # Next.js and React
    '.vercel', 'next-env.d.ts', '.eslintrc*', 'next.config.js', 'next-sitemap.config.js',
    'public/**', '.pnp.*', '*.pnp.js',

    # iOS and macOS Development
    '*.xcodeproj', '*.xcworkspace', '*.pbxproj', '*.mode1v3', '*.mode2v3', '*.perspectivev3',
    '*.xcuserstate', '*.xccheckout', '*.moved-aside', '*.hmap', '*.ipa', '*.dSYM.zip', '*.dSYM',
    'timeline.xctimeline', 'playground.xcworkspace', '.build/', 'DerivedData/', '*.playgroundbook',
    'Pods/', 'Carthage/Build',

    # Android Development
    '*.iml', '.gradle', 'local.properties', '.idea/caches', '.idea/libraries', '.idea/modules.xml',
    '.idea/workspace.xml', '.idea/navEditor.xml', '.idea/assetWizardSettings.xml', '.externalNativeBuild',
    '.cxx', '*.apk', '*.aab', '*.ap_', '*.dex',

    # Ruby on Rails
    '*.rbc', 'capybara-*.html', '.rspec', 'public/system', 'spec/tmp', '**.orig',
    'rerun.txt', 'pickle-email-*.html', '.bundle', 'vendor/bundle', 'log/*', 'tmp/*',
    'storage/*', '.byebug_history', 'config/master.key', 'config/credentials.yml.enc',

    # Java
    '*.class', '*.war', '*.ear', '*.jar', 'hs_err_pid*', '.mtj.tmp/',

    # Python
    '*.egg-info/', 'pip-log.txt', 'pip-delete-this-directory.txt', '.tox/',
    '.coverage', '.coverage.*', '.cache', '*.cover', '*.py,cover', '.hypothesis/',
    'pytestdebug.log', '.python-version', '.mypy_cache', '.dmypy.json', '.pyre/',

    # Go
    '*.exe', '*.test', '*.prof', '*.out',

    # Rust
    'target/', 'Cargo.lock', '**/*.rs.bk',

    # .NET
    '[Bb]in/', '[Oo]bj/', '[Ll]og/', '[Ll]ogs/', '.vs/', '*_i.c', '*_p.c', '*_h.h', '*.ilk',
    '*.meta', '*.obj', '*.iobj', '*.pch', '*.pdb', '*.ipdb', '*.pgc', '*.pgd', '*.rsp', '*.sbr',
    '*.tlb', '*.tli', '*.tlh', '*.tmp', '*.tmp_proj', '*_wpftmp.csproj', '*.vspscc', '*.vssscc',

    # Unity
    '[Ll]ibrary/', '[Tt]emp/', '[Oo]bj/', '[Bb]uild/', '[Bb]uilds/', '[Ll]ogs/', '[Uu]ser[Ss]ettings/',
    '*.pidb.meta', '*.pdb.meta', '*.mdb.meta', '*.apk', '*.unitypackage', 'crashlytics-build.properties',

    # Jupyter Notebooks
    '.ipynb_checkpoints', '*/.ipynb_checkpoints/*', '*.ipynb',

    # R
    '.Rhistory', '.Rapp.history', '.RData', '.Ruserdata', '*-Ex.R', '/*.tar.gz', '/*.Rcheck/',
    '.Rproj.user/', '*.Rproj',

    # Elm
    'elm-stuff/', '*.elmo', '*.elmi',

    # Additional Patterns
    '.ropeproject', '.spyderproject', '.spyproject', '.webassets-cache', '.scrapy',
    'celerybeat-schedule', 'celerybeat.pid', '*.sage.py', '.venv', 'env/', 'venv/', 'ENV/',
    '.tern-port', '.vscode-test', '.yarn-integrity', '.expo/', '.expo-shared/',
    '*.jks', '*.keystore', '*.mobileprovision', '*.provisionprofile',
    '.sonar', '.scannerwork', '.terraform', '*.tfstate', '*.tfstate.*', '.vagrant',
    '*.bak', '*.gho', '*.ori', '*.orig', '.Trash-*', '$RECYCLE.BIN/', 'System Volume Information',
    '*.lnk', '.fseventsd', '.apdisk', '*.patch', '*.diff', '*.kicad_pcb-bak', '*.sch-bak',
    '~$*.doc*', '~$*.xls*', '~$*.ppt*', '*.~vsd*', '.~lock.*#', 'Thumbs.db:encryptable',
    '*.stackdump', '[Dd]esktop.ini', '*.code-snippets', '.atom/', '.tags', '.tags_sorted_by_file',
    '.gemtags', 'tags', 'TAGS', 'cscope.*', '*.rsuser', '*.pid', '*.seed', '*.pid.lock',
]
def list_directory(dir_path, gitignore_matcher, patterns, prefix="", current_depth=0, max_depth=4):
    if current_depth > max_depth:
        return []

    try:
        items = os.listdir(dir_path)
    except PermissionError:
        return [f"{prefix}[Permission Denied]"]

    structure = []
    for item in sorted(items):
        item_path = os.path.join(dir_path, item)
        if should_include_file(item_path, gitignore_matcher, patterns):
            structure.append(f"{prefix}{item}")
            if os.path.isdir(item_path):
                structure.extend(list_directory(item_path, gitignore_matcher, patterns,
                                                prefix + "│   ", current_depth + 1, max_depth))
    return structure

class DropZone(QLabel):
    folder_dropped = pyqtSignal(str)

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
        if files and os.path.isdir(files[0]):
            self.folder_dropped.emit(files[0])

    def set_folder(self, folder):
        self.setText(f"Selected Folder:\n{folder}")

    def clear_folder(self):
        self.setText('\n\n Drop Project Folder Here \n\n')

class AICodeMergeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.custom_output_file = None
        self.selected_folder = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.dropzone = DropZone()
        self.dropzone.folder_dropped.connect(self.set_folder)
        layout.addWidget(self.dropzone)

        folder_buttons_layout = QHBoxLayout()
        self.select_folder_button = QPushButton('Select Another Folder')
        self.select_folder_button.clicked.connect(self.select_folder)
        folder_buttons_layout.addWidget(self.select_folder_button)

        self.remove_folder_button = QPushButton('Remove Folder')
        self.remove_folder_button.clicked.connect(self.remove_folder)
        folder_buttons_layout.addWidget(self.remove_folder_button)

        layout.addLayout(folder_buttons_layout)

        form_layout = QVBoxLayout()

        # Max depth
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel('Max Depth:'))
        self.max_depth_input = QSpinBox()
        self.max_depth_input.setRange(1, 100)
        self.max_depth_input.setValue(4)
        depth_layout.addWidget(self.max_depth_input)
        form_layout.addLayout(depth_layout)

        # Max file size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel('Max File Size (KB):'))
        self.max_size_input = QSpinBox()
        self.max_size_input.setRange(1, 10000)
        self.max_size_input.setValue(100)
        size_layout.addWidget(self.max_size_input)
        form_layout.addLayout(size_layout)

        # File patterns
        patterns_layout = QHBoxLayout()
        patterns_layout.addWidget(QLabel('File Patterns (comma-separated):'))
        self.patterns_input = QLineEdit('*')
        patterns_layout.addWidget(self.patterns_input)
        form_layout.addLayout(patterns_layout)

        # Exclude patterns
        exclude_layout = QHBoxLayout()
        exclude_layout.addWidget(QLabel('Exclude Patterns:'))
        self.exclude_input = QTextEdit()
        self.exclude_input.setPlainText('\n'.join(DEFAULT_EXCLUDE_PATTERNS))
        self.exclude_input.setToolTip("Click to edit. Use 'Reset to Defaults' to restore original patterns.")
        self.exclude_input.setFixedHeight(100)  # Adjust this value to fit 5 lines
        exclude_layout.addWidget(self.exclude_input)
        self.reset_exclude_button = QPushButton('Reset to Defaults')
        self.reset_exclude_button.clicked.connect(self.reset_exclude_patterns)
        exclude_layout.addWidget(self.reset_exclude_button)
        form_layout.addLayout(exclude_layout)

        # Add output file selection
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel('Output File:'))
        self.output_file_input = QLineEdit()
        self.output_file_input.setPlaceholderText('Default: ProjectName_Timestamp.md')
        output_layout.addWidget(self.output_file_input)
        self.output_file_button = QPushButton('Browse')
        self.output_file_button.clicked.connect(self.select_output_file)
        output_layout.addWidget(self.output_file_button)
        form_layout.addLayout(output_layout)

        layout.addLayout(form_layout)

        self.start_button = QPushButton('Start Process')
        self.start_button.clicked.connect(self.start_process)
        layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle('AICodeMerge')
        self.setGeometry(300, 300, 600, 500)  # Increased height to accommodate new elements

    def set_folder(self, folder):
        self.selected_folder = folder
        self.dropzone.set_folder(folder)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.set_folder(folder)

    def remove_folder(self):
        self.selected_folder = None
        self.dropzone.clear_folder()

    def reset_exclude_patterns(self):
        self.exclude_input.setPlainText('\n'.join(DEFAULT_EXCLUDE_PATTERNS))

    def select_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "Markdown Files (*.md);;All Files (*)")
        if file_name:
            self.custom_output_file = file_name
            self.output_file_input.setText(file_name)

    def start_process(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "No Folder Selected", "Please select a project folder before starting the process.")
            return

        self.process_folder(self.selected_folder)

    def process_folder(self, folder_path):
        if not os.access(folder_path, os.R_OK):
            QMessageBox.critical(self, "Permission Denied", f"Cannot access the folder: {folder_path}\nPlease check your permissions and try again.")
            return

        # Get values from input fields
        max_depth = self.max_depth_input.value()
        max_size = self.max_size_input.value()
        patterns = [p.strip() for p in self.patterns_input.text().split(',')]
        exclude_patterns = [p.strip() for p in self.exclude_input.toPlainText().split('\n') if p.strip()]

        # Determine output file
        if self.custom_output_file:
            output_file = self.custom_output_file
        else:
            project_name = os.path.basename(os.path.abspath(folder_path))
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{project_name}_{timestamp}.md"

        self.progress_bar.setValue(0)

        try:
            self.run_aicodemerge(folder_path, output_file, max_depth, max_size, patterns, exclude_patterns)
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Process Complete", f"AICodeMerge has finished processing the folder.\nOutput file: {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Processing Error", f"An error occurred while processing: {str(e)}")

    def run_aicodemerge(self, project_path, output_file, max_depth, max_size, patterns, exclude_patterns):
        gitignore_matcher = parse_gitignore(os.path.join(project_path, '.gitignore'), exclude_patterns)
        
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("# Project Knowledge for AI Analysis\n\n")
            out.write("This markdown file contains the structure and contents of a project. ")
            out.write("It is organized as follows:\n\n")
            out.write("1. Project folder structure\n")
            out.write("2. Contents of relevant files\n\n")
            out.write("---\n\n")
            out.write("## Project Configuration\n\n")
            out.write(f"- Max directory depth: {max_depth}\n")
            out.write(f"- Max file size: {max_size}KB\n")
            out.write(f"- File patterns included: {', '.join(patterns)}\n\n")
            out.write("---\n\n")
            out.write("## Project Folder Structure\n\n")
            
            # Generate and write the folder structure
            structure = list_directory(project_path, gitignore_matcher, patterns, max_depth=max_depth)
            out.write("\n".join(structure))
            
            out.write("\n\n## File Contents\n")

        files_to_process = []
        for root, _, files in os.walk(project_path):
            if any(exclude in root.split(os.path.sep) for exclude in exclude_patterns):
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
        return output_file

def main():
    app = QApplication(sys.argv)
    ex = AICodeMergeGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
