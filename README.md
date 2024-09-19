# AI Code Merge

AI Code Merge is a tool for concatenating codebases and preparing them for input into AI systems. It combines multiple code files from projects or repositories to facilitate codebase analysis or documentation generation.

## Features

- Concatenate multiple code files into a single file
- Support for various file types
- Customizable file inclusion/exclusion
- Command-line interface
- Simple graphical user interface (early phase, incomplete)

## Components

1. `aicodemerge.py`: Core script for merging code files (CLI functionality)
2. `aicodemerge-gui.py`: Graphical interface for the AI Code Merge tool (early phase, incomplete)

## Installation

1. Ensure Python 3.6 or later is installed.

2. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-code-merge.git
   cd ai-code-merge
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

Run:

```
python aicodemerge.py [options] [file/directory paths]
```

Options:
- `-d, --max-depth`: Maximum depth for directory traversal
- `-s, --max-size`: Maximum file size in KB to include
- `-p, --patterns`: File patterns to include
- `-o, --output`: Specify the output file name
- `-v, --verbose`: Enable verbose output
- `-c, --custom`: Use custom configuration mode

Example:
```
python aicodemerge.py -d 4 -s 100 -p "*.py,*.js" -o output.md ./project
```

### Graphical User Interface (Early Phase)

The GUI is currently in an early development phase and is incomplete. Basic functionality includes:

Run:
```
python aicodemerge-gui.py
```

- Select a project folder
- Process the folder and generate output

Note: The GUI version is still under development and may lack features or stability compared to the CLI version.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please file an issue on the GitHub repository.
