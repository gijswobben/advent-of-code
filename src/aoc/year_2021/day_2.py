# https://adventofcode.com/2021/day/2

from pathlib import Path


def part_one(input_lines: list[str]) -> int:
    """Calculate a final output based on a set of instructions.

    Args:
        input_lines (list[str]): List of instructions.

    Raises:
        Exception: Raised when an unknown instruction is found.

    Returns:
        int: The final output.
    """

    # Parse the instructions
    elements = [line.split(" ") for line in input_lines]
    instructions = [(direction, int(units)) for direction, units in elements]

    # Follow the instructions
    horizontal_position = 0
    depth = 0
    for direction, units in instructions:
        if direction == "forward":
            horizontal_position += units
        elif direction == "down":
            depth += units
        elif direction == "up":
            depth -= units
        else:
            raise Exception("Unexpected instruction")

    return horizontal_position * depth


def part_two(input_lines: list[str]) -> int:
    """Calculate a final output based on a set of instructions based on
    aim.

    Args:
        input_lines (list[str]): List of instructions.

    Raises:
        Exception: Raised when an unknown instruction is found.

    Returns:
        int: The final output.
    """

    # Parse the instructions
    elements = [line.split(" ") for line in input_lines]
    instructions = [(direction, int(units)) for direction, units in elements]

    # Follow the instructions
    horizontal_position = 0
    depth = 0
    aim = 0
    for direction, units in instructions:
        if direction == "forward":
            horizontal_position += units
            depth += aim * units
        elif direction == "down":
            aim += units
        elif direction == "up":
            aim -= units
        else:
            raise Exception("Unexpected instruction")

    return horizontal_position * depth


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_2.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
