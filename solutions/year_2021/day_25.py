# https://adventofcode.com/2021/day/25

from pathlib import Path


def part_one(input_lines: list[str]) -> int:
    return 0


def part_two(input_lines: list[str]) -> int:
    return 0


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_25.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)