# https://adventofcode.com/2022/day/4

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Assignment:
    start: int
    end: int

    @property
    def range(self) -> set[int]:
        return set(range(self.start, self.end + 1))

    @classmethod
    def from_string(self, input_string: str) -> Assignment:
        start, end = [int(element) for element in input_string.split("-")]
        return Assignment(start=start, end=end)

    def includes(self, other: Assignment) -> bool:
        return len(other.range - self.range) == 0


def parse_input(line: str) -> tuple[Assignment, Assignment]:
    elf_one, elf_two = [
        Assignment.from_string(input_string) for input_string in line.split(",")
    ]
    return elf_one, elf_two


def part_one(input_lines: list[str]) -> int:

    # Loop all the assignments
    total = 0
    for line in input_lines:

        # Parse the assignment
        assignment_a, assignment_b = parse_input(line)

        # Increment if either of the assignment includes the other
        # completely
        if assignment_a.includes(assignment_b) or assignment_b.includes(assignment_a):
            total += 1

    return total


def part_two(input_lines: list[str]) -> int:

    # Loop all the assignments
    total = 0
    for line in input_lines:

        # Parse the assignment
        assignment_a, assignment_b = parse_input(line)

        # If the combination of elements in both assignment is not equal
        # to the sum of items in each assignment there is overlap
        if len(assignment_a.range | assignment_b.range) != (
            len(assignment_a.range) + len(assignment_b.range)
        ):
            total += 1

    return total


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[2] / "data/year_2022/day_4.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
