# https://adventofcode.com/2022/day/3

import functools
import string
from pathlib import Path

SCORE: dict[str, int] = {
    character: index + 1
    for index, character in enumerate(string.ascii_lowercase + string.ascii_uppercase)
}


class Rucksack:
    """Represents a single rucksack of an elf. Each Rucksack has 2
    compartments that hold half of the items the elf is carrying.

    Args:
        items (list[str]): List of items the elf is carrying.
    """

    def __init__(self, items: list[str]) -> None:
        self.compartments: tuple[list[str], list[str]] = (
            items[: len(items) // 2],
            items[len(items) // 2 :],
        )

    @property
    def items(self) -> list[str]:
        return self.compartments[0] + self.compartments[1]


def part_one(input_lines: list[str]) -> int:

    # Loop over the lines
    score = 0
    for line in input_lines:

        # Create a rucksack from the input line
        rucksack = Rucksack(items=list(line))

        # Find the common character in the compartments of the rucksack
        common = list(set(rucksack.compartments[0]) & set(rucksack.compartments[1]))

        # Lookup the score for the common character
        score += SCORE[common[0]]

    return score


def part_two(input_lines: list[str]) -> int:

    # Loop groups of 3 lines
    score = 0
    group_size = 3
    groups = zip(*(iter(input_lines),) * group_size)
    for group in groups:

        # Create a list of all the rucksacks in this group
        rucksacks = [Rucksack(items=list(elf)) for elf in group]

        # Determine the common character in the rucksacks of this group
        common = list(
            functools.reduce(
                lambda a, b: a.intersection(b),  # type: ignore
                [set(rucksack.items) for rucksack in rucksacks],
            )
        )

        # Lookup the score for the common character
        score += SCORE[common[0]]

    return score


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_3.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
