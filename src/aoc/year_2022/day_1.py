# https://adventofcode.com/2022/day/1

from pathlib import Path


def parse_input(input_lines: list[str]) -> list[int]:
    """Method that combines groups of lines, separated by an empty line,
    and sums the results.

    Args:
        input_lines (list[str]): List of strings with one number by line
            and blank lines as separator.

    Returns:
        list[int]: List of total calories per elf.
    """
    output: list[int] = []
    buffer: int = 0
    for line in input_lines:

        # Found a separator, reset the buffer and add the result
        if line == "":
            output.append(buffer)
            buffer = 0

        # Add the number to the buffer
        else:
            buffer += int(line)

    # Add the last one before returning
    output.append(buffer)
    return output


def part_one(input_lines: list[str]) -> int:
    result = parse_input(input_lines=input_lines)
    return max(result)


def part_two(input_lines: list[str]) -> int:
    result = sorted(parse_input(input_lines=input_lines), reverse=True)
    return sum(result[:3])


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_1.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output
    result = part_one(input_lines)
    print("Part one:", result)

    result = part_two(input_lines)
    print("Part two:", result)
