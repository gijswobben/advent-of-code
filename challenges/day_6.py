# https://adventofcode.com/2022/day/6

from pathlib import Path


def part_one(input_line: str, buffer_length: int = 4) -> int:

    # Create a buffer of the first N characters
    buffer: list[str] = list(input_line[:buffer_length])

    # Loop the rest of the characters
    for index, character in enumerate(input_line[buffer_length:], start=buffer_length):

        # Check if there are only unique characters in the buffer
        if len(set(buffer)) == buffer_length:
            return index

        # Add one more character, remove the first (rolling buffer)
        buffer.append(character)
        buffer.pop(0)

    # Return the last index
    return index


def part_two(input_line: str) -> int:

    # Same as part one, just with a larger buffer
    return part_one(input_line, buffer_length=14)


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[1] / "data/day_6.txt", "r") as f:
        input_line = f.read()

    # Determine the output for part one
    result = part_one(input_line)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_line)
    print("Part two:", result)
