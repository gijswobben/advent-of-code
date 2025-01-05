"""Assignment for day 1 of 2024 Advent of Code.

https://adventofcode.com/2024/day/1
"""

import math
from collections import Counter
from pathlib import Path


def input_to_lists(input_lines: list[str]) -> list[list[int]]:
    """Convert the input lines to lists of lists of integers.

    Args:
    ----
        input_lines (list[str]): The input lines.

    Returns:
    -------
        The list of lists of integers.

    """
    list_left: list[int] = []
    list_right: list[int] = []
    for line in input_lines:
        left, right = line.split()
        list_left.append(int(left))
        list_right.append(int(right))
    return [list_left, list_right]


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        The result for assignment one.

    """
    # Parse the input
    list_left, list_right = input_to_lists(input_lines)

    # Order both lists
    list_left.sort()
    list_right.sort()

    # Zip together the lists and calculate the distance between the
    # combined values
    return int(
        sum(
            [
                math.dist((left,), (right,))
                for left, right in zip(list_left, list_right)
            ],
        ),
    )


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        The result for assignment two.

    """
    # Parse the input
    list_left, list_right = input_to_lists(input_lines)

    counts = Counter(list_right)

    return int(sum([counts[left] * left for left in list_left]))


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2024/day_1.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
