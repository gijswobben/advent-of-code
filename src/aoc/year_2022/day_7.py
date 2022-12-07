# https://adventofcode.com/2022/day/7

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

CHANGE_DIRECTORY_REGEX = re.compile(r"\$\s*cd\s(?P<destination>.+)")

TOTAL_DISKSPACE = 70000000
UNUSED_SPACE_REQUIRED = 30000000


@dataclass
class File:
    """Class that represents a single file in the filesystem."""

    name: str
    size: int
    parent: Directory


class Directory:
    """A single directory in the filesystem.

    Args:
        name (str): The name of the directory.
        parent (Directory | None): The parent directory or None if this
            is the root. Defaults to None.
    """

    def __init__(self, name: str, parent: Directory | None = None) -> None:
        self.name = name
        self.parent = parent
        self.subdirectories: dict[str, Directory] = {}
        self.files: dict[str, File] = {}

    def to_directory_list(self) -> list[Directory]:
        """Convert this directory wiht subdirectories into a flat list
        of directories.

        Returns:
            list[Directory]: A flat list of all directories (recursive)
        """
        output: list[Directory] = [self]
        for subdirectory in self.subdirectories.values():
            output.extend(subdirectory.to_directory_list())
        return output

    @property
    def path(self) -> str:
        """Full absolute path to this directory.

        Returns:
            str: The full path as a string.
        """
        path: list[str] = []
        if self.parent is not None:
            path.append(self.parent.path)
        path.append(self.name)
        return "/" + ("/".join(path).lstrip("/"))

    @property
    def size(self) -> int:
        """Size of this directory.

        Returns:
            int: The total directory size as an integer.
        """
        return sum(
            [file.size for file in self.files.values()]
            + [directory.size for directory in self.subdirectories.values()]
        )

    def __repr__(self) -> str:
        return f"Directory<name={self.name}, size={self.size}>"

    def to_string(self, n_indent_spaces: int = 2) -> str:
        """Method to get the full directory tree as a string (for
        debugging purposes.)

        Args:
            n_indent_spaces (int): The number of spaces to use for
                indentation of the different levels in the tree.
                Defaults to 2.

        Returns:
            str: The full directory structure (tree) as a string.
        """

        def _recurse(directory: Directory, level: int = 0) -> list[str]:
            indent = " " * (2 * level)
            output: list[str] = [f"{indent}- {directory.name} (dir)"]

            for subdirectory in directory.subdirectories.values():
                output.extend(_recurse(subdirectory, level=level + 1))

            for file in directory.files.values():
                output.append(f"{indent}  - {file.name} (file, size={file.size})")

            return output

        return "\n".join(_recurse(self))


def terminal_output_parser(input_lines: list[str]) -> Directory:
    """Parser that converts terminal output to a directory structure.

    Args:
        input_lines (list[str]): The terminal output as a list of
        strings.

    Raises:
        Exception: Raised when an invalid line was encountered in the
            input.

    Returns:
        Directory: The parsed root directory of the output.
    """
    root = Directory(name="/")
    active_directory: Directory | None = None
    for line in input_lines:

        # Parse a command
        if line.startswith("$ cd "):

            # Extract the destination of the CD command
            match = re.match(CHANGE_DIRECTORY_REGEX, line)
            if match is not None:
                destination = match.group("destination")
            else:
                raise Exception("Invalid cd command")

            # Set the active directory to the destination directory
            if destination == "/":
                active_directory = root
            elif destination == "..":
                if active_directory is None:
                    raise Exception("No active directory, cannot perform relative cd.")
                active_directory = active_directory.parent
            else:
                if active_directory is None:
                    raise Exception("No active directory, cannot perform relative cd.")
                active_directory = active_directory.subdirectories[destination]

        # Skip ls commands (provide no info)
        elif line.startswith("$ ls"):
            pass

        # Parse a new file/directory
        else:
            if line.startswith("dir "):
                if active_directory is None:
                    raise Exception(
                        "Invalid output encountered. "
                        "No active directory but found a subdirectory."
                    )
                _, directory_name = line.split(" ", maxsplit=2)
                new_directory = Directory(name=directory_name, parent=active_directory)
                active_directory.subdirectories[directory_name] = new_directory
            else:
                if active_directory is None:
                    raise Exception(
                        "Invalid output encountered. "
                        "No active directory but found a file."
                    )
                file_size, file_name = line.split(" ", maxsplit=2)
                new_file = File(file_name, int(file_size), active_directory)
                active_directory.files[file_name] = new_file

    # Return the root
    return root


def part_one(input_lines: list[str]) -> int:

    # Parse the terminal output
    root = terminal_output_parser(input_lines)

    # Sum all directory sizes of directories that are <= 100000 in size
    return sum(
        [
            directory.size
            for directory in root.to_directory_list()
            if directory.size <= 100_000
        ]
    )


def part_two(input_lines: list[str]) -> int:

    # Parse the terminal output
    root = terminal_output_parser(input_lines)

    # Calculate the currently unused diskspace and the total size of
    # folders that have to be removed before we can run the update
    current_unused_space = TOTAL_DISKSPACE - root.size
    min_size_to_remove = UNUSED_SPACE_REQUIRED - current_unused_space

    # Get a list of candidate directories to delete and sort them by
    # size
    candidates = sorted(root.to_directory_list(), key=lambda directory: directory.size)

    # Return the first candidate that is big enough
    for candidate in candidates:
        if candidate.size >= min_size_to_remove:
            return candidate.size
    return 0


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_7.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
