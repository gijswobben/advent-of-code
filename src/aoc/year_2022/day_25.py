# https://adventofcode.com/2022/day/25

from pathlib import Path


class SNAFU:
    """SNAFU number encoder/decoder."""

    _mapping: dict[str, int] = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2,
    }

    _reverse_mapping: dict[int, str] = {
        2: "2",
        1: "1",
        0: "0",
        -1: "-",
        -2: "=",
    }

    @staticmethod
    def encode(number: int) -> str:
        """Encode a decimal number in a SNAFU number.

        Args:
            num (int): The decimal input number.

        Returns:
            str: The SNAFU number.
        """

        def _to_base_5(num: int) -> str:
            base_5_number = ""
            while num:
                base_5_number = str(num % 5) + base_5_number
                num //= 5
            return base_5_number

        # Convert the decimal number to a base 5 number (like SNAFU)
        base_5_numbers: list[int] = [int(character) for character in _to_base_5(number)]

        # Go over all the numbers (right to left)
        snafu: list[int] = []
        for index in range(len(base_5_numbers) - 1, -1, -1):
            element = base_5_numbers[index]

            # If the number is in the SNAFU system, use it
            if element <= 2:
                snafu.insert(0, element)

            # Increase the next number and insert the negative remainder
            # + 1, to shift to the next number
            else:
                base_5_numbers[index - 1] += 1
                snafu.insert(0, -((element % 2) + 1))

        # Convert the base 5 numbers with negative values to SNAFU
        return "".join([SNAFU._reverse_mapping[element] for element in snafu])

    @staticmethod
    def decode(number: str) -> int:
        """Decode a SNAFU number to decimal.

        Args:
            number (str): The SNAFU number.

        Returns:
            int: The decimal representation.
        """

        # Map all characters to real numbers
        numbers: list[int] = [SNAFU._mapping[character] for character in number]

        # Sum the number times its base 5 position
        return sum(
            [
                number * 5**position
                for number, position in zip(numbers, range(len(numbers) - 1, -1, -1))
            ]
        )


def part_one(input_lines: list[str]) -> str:

    # Decode all the numbers and add them up
    total = sum([SNAFU.decode(number) for number in input_lines])

    # Encode the total
    return SNAFU.encode(total)


def part_two(input_lines: list[str]) -> int:
    return 0


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_25.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result_two = part_two(input_lines)
    print("Part two:", result_two)
