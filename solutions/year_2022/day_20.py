# https://adventofcode.com/2022/day/20

from pathlib import Path


class File:
    """Represents a file with encrypted content.

    Main idea is to modify a list of positions of each number in the
    original file contents, instead of modifying the content directly.

    Args:
        contents (list[int]): The (encrypted) file contents.
        decryption_key (int): A number that represents the decryption
            key. Defaults to 1.
        mixing_rounds (int, optional): The number of rounds to use
                for decrypting the file. Defaults to 1.
    """

    def __init__(
        self, contents: list[int], decryption_key: int = 1, mixing_rounds: int = 1
    ) -> None:
        self.original_contents = contents
        self.decrypted_contents: list[int] = self._decrypt(
            contents=contents,
            decryption_key=decryption_key,
            mixing_rounds=mixing_rounds,
        )

    def _decrypt(
        self, contents: list[int], decryption_key: int, mixing_rounds: int = 1
    ) -> list[int]:

        # Use the decryption key to decrypt all the values
        decrypted = [key * decryption_key for key in contents]

        # Store the positions of the numbers in the file content
        positions = list(range(len(decrypted)))

        # Define an alternative modulo function (%) that returns
        # negative remainders (like in may other languages)
        modulo = lambda n, base: n - int(n / base) * base

        # Repeat for the number of mixing rounds that should be
        # performed
        for _ in range(mixing_rounds):

            # Loop over all the numbers in the original contents
            for index, value in enumerate(decrypted):

                # Determine the new position of this number
                current_position = positions.index(index)
                new_position = modulo((current_position + value), (len(positions) - 1))

                # Inserting before 0 means insert at the end
                if new_position == 0:
                    new_position = len(positions)

                # Move the positions
                positions.insert(new_position, positions.pop(current_position))

        # Return the decrypted content by reordering the decrypted
        # numbers using the positions
        return [decrypted[i] for i in positions]

    def get(self, position: int) -> int:
        """Get the decrypted value N positions after the position of 0.

        Args:
            position (int): The position to retrieve.

        Returns:
            int: The decrypted value
        """
        sequence = self.decrypted_contents
        zero_index = sequence.index(0)
        sequence = sequence[zero_index:] + sequence[:zero_index]
        return sequence[position % (len(sequence))]


def part_one(input_lines: list[str]) -> int:
    file_contents = [int(line) for line in input_lines]
    file = File(file_contents)
    return file.get(1000) + file.get(2000) + file.get(3000)


def part_two(input_lines: list[str]) -> int:
    file_contents = [int(line) for line in input_lines]
    file = File(file_contents, decryption_key=811589153, mixing_rounds=10)
    return file.get(1000) + file.get(2000) + file.get(3000)


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_20.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
