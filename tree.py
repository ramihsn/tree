from configparser import ConfigParser
from argparse import ArgumentParser
from functools import partial
from pathlib import Path
import platform
import logging

logger = logging.getLogger("Tree")

# Default directories to exclude from the tree output
if Path('.tree.ini').exists():
    (config := ConfigParser()).read('.tree.ini')
    _DEFAULT_FILTERED_DIRS = config['filter'].get('exclude', '').split(',')
else:
    _DEFAULT_FILTERED_DIRS = ['.venv', '.pytest_cache', '__pycache__', '.git', '.vscode', 'node_modules']
_DEFAULT_FILTERED_DIRS = [Path(item) for item in _DEFAULT_FILTERED_DIRS]


class PathList(list[Path]):
    def __contains__(self, key: Path) -> bool:
        if not super().__contains__(key):
            return key.stem in [item.name for item in self]
        return True


def _print_folders(dirs: list[Path], indent: str, files: bool = False, exclude_dirs=None, folders_first=False):
    '''
    Print directories in a tree structure.

    Args:
        dirs (list[Path]): List of directory paths to print.
        indent (str): Current indentation level.
        files (bool): Indicates if there are files in the current directory.
        exclude_dirs (list[str]): List of directories to exclude.
        folders_first (bool): Flag indicating if folders should be printed before files.
    '''
    for i, dir in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1)
        # Determine the pointer symbol based on the position of the directory
        pointer = '└── ' if is_last_dir and not (folders_first or not files) else '├── '

        logger.info(f"{indent}{pointer}{dir.name}")
        extension = '    ' if pointer == '└── ' else '│   '
        _print_tree(dir, indent + extension, exclude_dirs, folders_first)


def _print_files(files: list[Path], indent: str, dirs: bool = False, folders_first=False):
    '''
    Print files in a tree structure.

    Args:
        files (list[Path]): List of file paths to print.
        indent (str): Current indentation level.
        dirs (bool): Indicates if there are directories in the current directory.
        folders_first (bool): Flag indicating if folders should be printed before files.
    '''
    for i, file in enumerate(files):
        is_last_file = (i == len(files) - 1)
        # Determine the pointer symbol based on the position of the file
        pointer = '└── ' if is_last_file and (folders_first or not dirs) else '├── '
        logger.info(f"{indent}{pointer}{file.name}")


def _sort_key(p: Path, folders_first: bool):
    '''
    Determine the sort key based on whether folders should be listed first.

    Args:
        p (Path): The path to determine the sort key for.
        folders_first (bool): Flag indicating if folders should be sorted before files.

    Returns:
        tuple: Sort key for the given path.
    '''
    if folders_first:
        # Sort by directories first, then by name
        return (p.is_dir(), p.name.lower())
    # Sort by files first, then by name
    return (p.is_file(), p.name.lower())


def _print_tree(dir_path: Path, indent: str = "", exclude_dirs: PathList[Path] = None, folders_first: bool = False):
    '''
    Recursively print the directory tree.

    Args:
        dir_path (Path): The root directory path to start the tree.
        indent (str): Current indentation level.
        exclude_dirs (list[str]): List of directories to exclude.
        folders_first (bool): Flag indicating if folders should be printed before files.
    '''
    if not dir_path.is_dir():
        return

    # Sort contents based on the folders_first flag
    contents = sorted(dir_path.iterdir(), key=partial(_sort_key, folders_first=folders_first))

    files = [item for item in contents if item.is_file()]
    dirs = [item for item in contents if item.is_dir() and item not in exclude_dirs]

    if folders_first:
        _print_folders(dirs, indent, files, exclude_dirs, folders_first)
        _print_files(files, indent, dirs, folders_first)
    else:
        _print_files(files, indent, dirs, folders_first)
        _print_folders(dirs, indent, files, exclude_dirs, folders_first)


def _parse_args():
    '''
    Parse command line arguments.

    Returns:
        Namespace: Parsed arguments.
    '''
    parser = ArgumentParser(description="Print the directory tree")
    parser.add_argument("-r", '--root', type=Path, default=Path('.'),
                        help="The root directory to start the tree, defaults to the current directory.")
    parser.add_argument('-f', '--filter', nargs='*', default=_DEFAULT_FILTERED_DIRS, type=Path,
                        help="List of directories to exclude. If no arguments are provided, "
                             "the default excludes are used. To include all directories, "
                             "pass an empty string (e.g., -f ''). "
                             f"(default: {[i.name for i in _DEFAULT_FILTERED_DIRS]}")
    parser.add_argument('-F', '--folders-first', action='store_true',
                        help="Print folders before files. (default: %(default)s)")
    parser.add_argument('-o', '--output-file', dest='file',
                        help="Save the output to a file. (default: %(default)s)")
    return parser.parse_args()


def main():
    """
    Main function to execute the directory tree printing.
    """
    args = _parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(args.file, mode='w', encoding='utf-8'),
        ] if args.file else None
    )

    root: Path = args.root.resolve()
    logger.info(root.name)
    _print_tree(args.root, "", PathList(args.filter), args.folders_first)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        import sys
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

    main()
