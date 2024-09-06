# AI Code Merge

AI Code Merge is a powerful tool designed to concatenate codebases and prepare them for input into AI systems. This project simplifies the process of combining multiple code files from various projects or repositories, making it easier to analyze large codebases or generate comprehensive documentation.

## Features

- Concatenate multiple code files into a single file
- Support for various programming languages
- Intelligent handling of comments and formatting
- Customizable output format
- Command-line interface for scripting and automation
- User-friendly graphical interface for easy interaction

## Components

1. `aicodemerge.py`: The core script for merging code files, offering command-line functionality.
2. `aicodemerge-gui.py`: A graphical user interface wrapper for the AI Code Merge tool, providing an intuitive user experience.

## Installation

1. Ensure you have Python 3.6 or later installed on your system.

2. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-code-merge.git
   cd ai-code-merge
   ```

3. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

To use the command-line interface, run:

```
python aicodemerge.py [options] [file/directory paths]
```

Options:
- `-o, --output`: Specify the output file (default: merged_output.txt)
- `-r, --recursive`: Recursively process directories
- `-e, --exclude`: Exclude file patterns (e.g., "*.txt,*.log")

Example:
```
python aicodemerge.py -o merged_project.txt -r ./project1 ./project2
```

### Graphical User Interface

To launch the GUI version, simply run:

```
python aicodemerge-gui.py
```

The GUI allows you to:
- Select input files or directories
- Choose output location and filename
- Set exclusion patterns
- View a preview of the merged output

## Contributing

We welcome contributions to the AI Code Merge project! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please ensure your code adheres to our coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to all contributors who have helped shape AI Code Merge
- Inspired by the need for efficient code analysis in AI applications

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.
