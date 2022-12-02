# https://adventofcode.com/2022/day/1

from typing import Generator


TEST_INPUT = [
    "1000",
    "2000",
    "3000",
    "",
    "4000",
    "",
    "5000",
    "6000",
    "",
    "7000",
    "8000",
    "9000",
    "",
    "10000",
]


def test_elves_calories():
    """Test based on the example provided in the challenge."""

    result = sorted(elves_calories(TEST_INPUT), reverse=True)
    assert max(result) == 24000
    assert sum(result[:3]) == 45000


def elves_calories(input_lines: list[str]) -> Generator[int, None, None]:
    """Method that combines groups of lines, separated by an empty line,
    and sums the results.

    Args:
        input_lines (list[str]): list of strings with one number by line
            and blank lines as separator.

    Returns:
        list[int]: list of total calories per elf.
    """
    buffer: int = 0
    for line in input_lines:
        if line == "":
            yield buffer
            buffer = 0
        else:
            buffer += int(line)
    yield buffer


if __name__ == "__main__":

    # Read the input
    with open("day_1.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output
    result = sorted(elves_calories(input_lines), reverse=True)
    print("Part one:", max(result))
    print("Part two:", sum(result[:3]))
