"""Assignment for day 11 of 2024 Advent of Code.

https://adventofcode.com/2024/day/11
"""

from pathlib import Path


class StoneRow:
    def __init__(self, row: str):
        self.stones = [int(element) for element in row.split(" ")]

    def blink(self) -> None:
        # Make a copy of the current row
        new_stones: list[int] = []

        # Iterate over the stones
        for stone_value in self.stones:
            # If the stone is engraved with the number 0, it is replaced
            # by a stone engraved with the number 1.
            if stone_value == 0:
                new_stones.append(1)

            # If the stone is engraved with a number that has an even
            # number of digits, it is replaced by two stones. The left
            # half of the digits are engraved on the new left stone, and
            # the right half of the digits are engraved on the new right
            # stone. (The new numbers don't keep extra leading zeroes:
            # 1000 would become stones 10 and 0.)
            elif len(str(stone_value)) % 2 == 0:
                string_value = str(stone_value)
                new_stones.append(int(string_value[: len(string_value) // 2]))
                new_stones.append(int(string_value[len(string_value) // 2 :]))

            # If none of the other rules apply, the stone is replaced by
            # a new stone; the old stone's number multiplied by 2024 is
            # engraved on the new stone.
            else:
                new_stones.append(stone_value * 2024)

        # Update the stones
        self.stones = new_stones


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    # Create the stone row
    stone_row = StoneRow(input_lines[0])

    # Blink the stone row
    for _ in range(25):
        stone_row.blink()

    # Return the number of stones
    return len(stone_row.stones)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    # Create the stone row
    stone_row = StoneRow(input_lines[0])

    # Blink the stone row
    for _ in range(75):
        stone_row.blink()

    # Return the number of stones
    return len(stone_row.stones)


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_11.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
