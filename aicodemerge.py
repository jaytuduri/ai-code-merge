#!/usr/bin/env python3

import os
import argparse
import fnmatch
import datetime
import re

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

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate a Markdown file containing the structure and contents of a project.")
    parser.add_argument("project_path", help="Path to the project directory")
    parser.add_argument("-d", "--max-depth", type=int, default=4, help="Maximum depth for directory traversal (default: 4)")
    parser.add_argument("-s", "--max-size", type=int, default=100, help="Maximum file size in KB to include (default: 100)")
    parser.add_argument("-p", "--patterns", default="*", help="File patterns to include, comma-separated (default: *)")
    parser.add_argument("-o", "--output", help="Specify the output file name (default: PROJECT_NAME_TIMESTAMP.md)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-c", "--custom", action="store_true", help="Use custom configuration mode")
    return parser.parse_args()

def custom_config():
    print("Welcome to the custom configuration mode!")
    
    max_depth = int(input("Enter maximum directory depth (default is 4): ") or 4)
    max_size = int(input("Enter maximum file size in KB (default is 100): ") or 100)
    patterns = input("Enter file patterns to include, comma-separated (default is *): ") or "*"
    
    exclude_patterns = DEFAULT_EXCLUDE_PATTERNS.copy()
    while True:
        print("\nCurrent exclusion patterns:")
        for i, pattern in enumerate(exclude_patterns, 1):
            print(f"{i}. {pattern}")
        
        choice = input("\nEnter a number to remove a pattern, 'a' to add a new pattern, or 'done' to finish: ")
        if choice.lower() == 'done':
            break
        elif choice.lower() == 'a':
            new_pattern = input("Enter new exclusion pattern: ")
            exclude_patterns.append(new_pattern)
        elif choice.isdigit() and 1 <= int(choice) <= len(exclude_patterns):
            del exclude_patterns[int(choice) - 1]
        else:
            print("Invalid input. Please try again.")
    
    return max_depth, max_size, patterns, exclude_patterns

def log_verbose(message, verbose):
    if verbose:
        print(message)

def parse_gitignore(gitignore_path, custom_exclude_patterns):
    patterns = custom_exclude_patterns.copy()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            patterns.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])

    def is_ignored(path):
        path = os.path.normpath(path)
        for pattern in patterns:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
        return False

    return is_ignored

def should_include_file(file_path, gitignore_matcher, patterns):
    return not gitignore_matcher(file_path) and any(fnmatch.fnmatch(os.path.basename(file_path), pattern) for pattern in patterns)

def list_directory(dir_path, prefix="", current_depth=0, max_depth=4, gitignore_matcher=None, patterns=None):
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
            if os.path.isdir(item_path) and item != 'node_modules':  # Explicitly skip node_modules
                structure.extend(list_directory(item_path, prefix + "│   ", current_depth + 1, max_depth, gitignore_matcher, patterns))
    return structure

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1][1:]

def append_file_content(file_path, output_file, max_size_kb):
    file_size_kb = os.path.getsize(file_path) / 1024
    if file_size_kb <= max_size_kb:
        with open(output_file, "a", encoding="utf-8") as out, open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            out.write(f"\n\n## File: {file_path}\n\n")
            out.write(f"```{get_file_extension(file_path)}\n")
            out.write(f.read())
            out.write("\n```\n")
    else:
        with open(output_file, "a", encoding="utf-8") as out:
            out.write(f"\n\n## File: {file_path}\n\n")
            out.write(f"File exceeds size limit ({file_size_kb:.2f}KB > {max_size_kb}KB). Content not included.\n")

def main():
    args = parse_arguments()

    if args.custom:
        max_depth, max_size, patterns, exclude_patterns = custom_config()
    else:
        max_depth = args.max_depth
        max_size = args.max_size
        patterns = args.patterns
        exclude_patterns = DEFAULT_EXCLUDE_PATTERNS

    if not os.path.isdir(args.project_path):
        print(f"Error: The specified project path '{args.project_path}' does not exist or is not a directory.")
        return

    project_name = os.path.basename(os.path.abspath(args.project_path))
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = args.output or f"{project_name}_{timestamp}.md"
    patterns = patterns.split(',')

    log_verbose(f"Project path: {args.project_path}", args.verbose)
    log_verbose(f"Output file: {output_file}", args.verbose)
    log_verbose(f"Max depth: {max_depth}", args.verbose)
    log_verbose(f"Max file size: {max_size}KB", args.verbose)
    log_verbose(f"File patterns: {patterns}", args.verbose)

    gitignore_matcher = parse_gitignore(os.path.join(args.project_path, '.gitignore'), exclude_patterns)

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
        
        structure = list_directory(args.project_path, max_depth=max_depth, gitignore_matcher=gitignore_matcher, patterns=patterns)
        out.write("\n".join(structure))
        
        out.write("\n\n# File Contents\n")

    log_verbose("Project structure written to output file", args.verbose)

    files_to_process = []
    for root, _, files in os.walk(args.project_path):
        if 'node_modules' in root.split(os.path.sep):
            continue  # Skip node_modules folders
        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file_path, gitignore_matcher, patterns):
                files_to_process.append(file_path)

    log_verbose(f"Total files to process: {len(files_to_process)}", args.verbose)

    for i, file_path in enumerate(files_to_process, 1):
        append_file_content(file_path, output_file, max_size)
        if args.verbose:
            print(f"\rProcessing files: {i}/{len(files_to_process)}", end="", flush=True)

    if args.verbose:
        print()  # New line after progress

    print(f"Markdown file created: {output_file}")
    print(f"Location: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
