"""Assignment for day 3 of 2024 Advent of Code.

https://adventofcode.com/2024/day/3
"""

import re
from pathlib import Path


class ComputerProgram:
    """Represents a computer program with corrupted instructions."""

    def __init__(self, input_line: str) -> None:
        self.instructions = input_line

    def execute(self) -> int:
        """Execute the instructions and return the total of all mul operations."""
        matches = re.findall(r"mul\(\d+,\d+\)", self.instructions)
        total = 0
        for match in matches:
            a, b = re.findall(r"\d+", match)
            total += int(a) * int(b)
        return total

    def execute_conditional(self) -> int:
        """Execute the instructions and return the total of all mul operations."""
        # Add the implied do() at the beginning of the instructions and
        # don't() at the end
        instructions = "do()" + self.instructions + "don't()"

        total = 0

        # Find all operations between do() and don't()
        matches = re.finditer(r"do\(\)(?P<instructions>.*?)(?=don't\(\))", instructions)
        for match in matches:
            # Get all mul operations within the do() and don't()
            matches = re.findall(r"mul\(\d+,\d+\)", match.group("instructions"))
            for m in matches:
                a, b = re.findall(r"\d+", m)
                total += int(a) * int(b)
        return total


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    return ComputerProgram("".join(input_lines)).execute()


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    return ComputerProgram("".join(input_lines)).execute_conditional()


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_3.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
