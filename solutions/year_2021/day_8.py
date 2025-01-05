# https://adventofcode.com/2021/day/8

from pathlib import Path

digits_map = {
    0: ["a", "b", "c", "e", "f", "g"],
    1: ["c", "f"],
    2: ["a", "c", "d", "e", "g"],
    3: ["a", "c", "d", "f", "g"],
    4: ["b", "c", "d", "f"],
    5: ["a", "b", "d", "f", "g"],
    6: ["a", "b", "d", "e", "f", "g"],
    7: ["a", "c", "f"],
    8: ["a", "b", "c", "d", "e", "f", "g"],
    9: ["a", "b", "c", "d", "f", "g"],
}


def decode_digit(input_line: str):

    # Create all possible mappings
    segment_map = {
        "a": ["a", "b", "c", "d", "e", "f", "g"],
        "b": ["a", "b", "c", "d", "e", "f", "g"],
        "c": ["a", "b", "c", "d", "e", "f", "g"],
        "d": ["a", "b", "c", "d", "e", "f", "g"],
        "e": ["a", "b", "c", "d", "e", "f", "g"],
        "f": ["a", "b", "c", "d", "e", "f", "g"],
        "g": ["a", "b", "c", "d", "e", "f", "g"],
    }

    digits: dict[int, str] = {}

    signal_pattern_raw, _ = input_line.split(" | ")
    signal_patterns = [
        "".join(sorted(element)) for element in signal_pattern_raw.split(" ")
    ]

    # Start by finding the 1's
    for signal_pattern in signal_patterns:
        if len(signal_pattern) == 2:
            digits[1] = signal_pattern
            for segment in digits_map[1]:
                segment_map[segment] = list(signal_pattern)

    # 7's
    for signal_pattern in signal_patterns:
        if len(signal_pattern) == 3:
            digits[7] = signal_pattern
            segment_map["a"] = list(set(signal_pattern) - set(digits[1]))

    # 8's
    for signal_pattern in signal_patterns:
        if len(signal_pattern) == 7:
            digits[8] = signal_pattern

    # 4's
    for signal_pattern in signal_patterns:
        if len(signal_pattern) == 4:
            digits[4] = signal_pattern

    # 3's
    for signal_pattern in signal_patterns:
        if len(signal_pattern) == 5 and len(set(signal_pattern) - set(digits[7])) == 2:
            digits[3] = signal_pattern

    # 9's
    for signal_pattern in signal_patterns:
        if len(signal_pattern) == 6 and len(set(signal_pattern) - set(digits[4])) == 2:
            digits[9] = signal_pattern

    # 0's
    for signal_pattern in signal_patterns:
        if (
            len(signal_pattern) == 6
            and signal_pattern != digits[9]
            and len(set(signal_pattern) - set(digits[7])) == 3
        ):
            digits[0] = signal_pattern

    # 6's
    for signal_pattern in signal_patterns:
        if (
            len(signal_pattern) == 6
            and signal_pattern != digits[9]
            and signal_pattern != digits[0]
        ):
            digits[6] = signal_pattern

    # 5's
    for signal_pattern in signal_patterns:
        if (
            len(signal_pattern) == 5
            and signal_pattern != digits[3]
            and len(set(signal_pattern) - set(digits[6])) == 0
        ):
            digits[5] = signal_pattern

    # 2's
    for signal_pattern in signal_patterns:
        if signal_pattern not in list(digits.values()):
            digits[2] = signal_pattern

    return digits


def count_digits(input_line: str, digits: dict[int, str | None]) -> dict[int, int]:

    reverse_digits: dict[str, int] = {
        value: key for key, value in digits.items() if value is not None
    }

    _, output_pattern_raw = input_line.split(" | ")
    output_patterns: list[str] = [
        "".join(sorted(element)) for element in output_pattern_raw.split(" ")
    ]

    counter: dict[int, int] = {i: 0 for i in range(10)}

    for pattern, digit in reverse_digits.items():
        for output_pattern in output_patterns:
            if sorted(output_pattern) == sorted(pattern):
                counter[digit] += 1

    return counter


def decode_output(input_line: str, digits: dict[int, str | None]) -> int:

    reverse_digits: dict[str, int] = {
        value: key for key, value in digits.items() if value is not None
    }

    _, output_pattern_raw = input_line.split(" | ")
    output_patterns: list[str] = [
        "".join(sorted(element)) for element in output_pattern_raw.split(" ")
    ]

    digit_string = ""
    for output_pattern in output_patterns:
        digit_string += str(reverse_digits[output_pattern])
    return int(digit_string)


def part_one(input_lines: list[str]) -> int:
    total = 0
    for line in input_lines:
        digits = decode_digit(line)
        counts = count_digits(line, digits=digits)
        total += counts[1] + counts[4] + counts[7] + counts[8]
    return total


def part_two(input_lines: list[str]) -> int:
    total = 0
    for line in input_lines:
        digits = decode_digit(line)
        output_number = decode_output(line, digits)
        total += output_number
    return total


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_8.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
