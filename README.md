# Directory Tree Printer

This script prints the directory tree of a specified root directory, with options to exclude certain directories and to choose the order in which files and directories are printed.

## Features

- Print the directory tree of a specified root directory.
- Exclude specific directories from the output.
- Option to print folders before files.

## Requirements

- Python 3.6 or higher

## Installation

1. Clone the repository or download the script.
2. Ensure you have Python installed on your system.

## Download Executables

You can download the pre-built executables for different platforms from the latest release:

- [Download for Windows](https://github.com/ramihsn/tree/releases/latest/download/tree.exe)
- [Download for Linux](https://github.com/ramihsn/tree/releases/latest/download/tree)

## Usage

Run the script with the desired options:

```sh
python tree_exclude.py [options]
```

### Options
* -r, --root ROOT: The root directory to start the tree. (default: the current working directory).
* -f, --filter FILTER: List of directories to exclude. If no arguments are provided, the default excludes are used. To include all directories, pass an empty string (e.g., -f ''). (default: ['.venv', '.pytest_cache', '__pycache__', '.git', '.vscode', 'node_modules'])
* -F, --folders-first: Print folders before files. (default: False)
* -o, --output-file FILE: Save the output to a file. (default: None)

## Examples
#### Without flags
```sh
py .\tree.py
tree
├── .flake8
├── README.md
├── tree.py
└── folder-1
    ├── file-1
    ├── file-2
    └── folder-2
        └── file-1
```
#### With reversing the print output
```sh
py .\tree.py -F
tree
├── folder-1
│   ├── folder-2
│   │   └── file-1
│   ├── file-1
│   └── file-2
├── .flake8
├── README.md
└── tree.py
```
#### With different root
```sh
py .\tree.py -r .\folder-1\
folder-1
├── file-1
├── file-2
└── folder-2
    └── file-1
```
#### With filter
```sh
py .\tree.py -f folder-2
tree
├── .flake8
├── README.md
├── tree.py
└── folder-1
    ├── file-1
    └── file-2
```
#### With removing all filters
```sh
py .\tree.py -f
tree
├── .flake8
├── README.md
├── tree.py
├── .git
│   ├── COMMIT_EDITMSG
│   ├── config
│   ├── FETCH_HEAD
│   ├── HEAD
│   ├── index
│   ├── hooks
│   │   └── pre-push
│   ├── logs
│   └── refs
│       ├── heads
│       │   └── main
│       ├── remotes
│       │   └── origin
│       │       └── main
│       └── tags
└── folder-1
    ├── file-1
    ├── file-2
    └── folder-2
        └── file-1
```

## Configuration
To configure the maximum line length for Flake8 to 120 characters, create a .flake8 file in the root directory of your project with the following content:

```ini
[flake8]
max-line-length = 120
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

## Author
Rami Hasan

[![LinkedIn Profile](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/rami-hassan)
