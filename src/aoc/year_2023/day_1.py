# https://adventofcode.com/2023/day/1

from pathlib import Path

WRITTEN_DIGITS: dict[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def to_digits(line: str) -> list[int]:
    digits: list[int] = []
    for index, char in enumerate(line):
        if char.isdigit():
            digits.append(int(char))
        else:
            for word, digit in WRITTEN_DIGITS.items():
                if line[index : index + len(word)] == word:
                    digits.append(digit)
    return digits


def part_one(input_lines: list[str]) -> int:
    digits_per_line = [to_digits(line) for line in input_lines]
    digits: list[int] = [int(f"{line[0]}{line[-1]}") for line in digits_per_line]
    return sum(digits)


def part_two(input_lines: list[str]) -> int:
    return part_one(input_lines)


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_1.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
