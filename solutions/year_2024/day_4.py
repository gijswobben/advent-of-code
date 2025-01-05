"""Assignment for day 4 of 2024 Advent of Code.

https://adventofcode.com/2024/day/4
"""

import re
from pathlib import Path


class WordSearch:
    def __init__(self, grid: list[str], target_words: list[str] = ["XMAS"]) -> None:
        self.grid = grid
        self.target_words = target_words

    @staticmethod
    def flip_grid_90(grid: list[str]) -> list[str]:
        """Flip the grid 90 degrees.

        Args:
        ----
            grid: The grid to flip.

        Returns:
        -------
            The flipped grid.

        """
        # Get the number of rows and columns
        num_rows = len(grid)
        num_cols = len(grid[0])

        # Create a new grid with flipped dimensions
        flipped_grid = [["" for _ in range(num_rows)] for _ in range(num_cols)]

        # Fill the new grid with the flipped values
        for i in range(num_rows):
            for j in range(num_cols):
                flipped_grid[j][num_rows - 1 - i] = grid[i][j]

        # Convert the flipped grid back to a list of strings
        return ["".join(row) for row in flipped_grid]

    def find_vertical(self, grid: list[str], word: str) -> int:
        """Find the target word in the vertical grid.

        Args:
        ----
            grid: The grid to search.
            word: The target word to search for.

        Returns:
        -------
            The total count of the target word in the grid.

        """
        total = 0
        for i in range(len(grid[0])):
            line = "".join([line[i] for line in grid])
            total += len(re.findall(rf"{word}", line))
            total += len(re.findall(rf"{word}", line[::-1]))
        return total

    def find_diagonal(self, grid, word: str) -> int:
        """Find the target word in the diagonal grid.

        Args:
        ----
            grid: The grid to search.
            word: The target word to search for.

        Returns:
        -------
            The total count of the target word in the grid.

        """
        # Initialize the total count
        total = 0

        # Add padding to the grid
        line_length = len(grid[0])
        padded_grid = ["." * line_length + line + "." * line_length for line in grid]

        # Shift the grid to the left and right to "undo" the diagonal
        padded_grid_shift_left = [
            line[row_index : -(line_length - row_index)]
            for row_index, line in enumerate(padded_grid)
        ]
        padded_grid_shift_right = [
            line[(line_length - row_index) : -row_index]
            for row_index, line in enumerate(padded_grid)
        ]

        # Treat the shifted grids as vertical grids
        total += self.find_vertical(padded_grid_shift_left, word)
        total += self.find_vertical(padded_grid_shift_right, word)
        return total

    def count_target_words(self) -> int:
        """Count the target words in the grid."""
        # Initialize the total count
        total = 0

        # Vertical search
        total += sum(
            [self.find_vertical(self.grid, word) for word in self.target_words],
        )

        # Horizontal search (vertical over a 90 degree flipped grid)
        total += sum(
            [
                self.find_vertical(self.flip_grid_90(self.grid), word)
                for word in self.target_words
            ],
        )

        # Diagonal search
        total += sum(
            [self.find_diagonal(self.grid, word) for word in self.target_words],
        )

        # Diagonal search over a rotated grid
        total += sum(
            [
                self.find_diagonal(
                    self.flip_grid_90(self.grid),
                    word,
                )
                for word in self.target_words
            ],
        )
        return total


class XMasWordSearch(WordSearch):
    def is_x_mas(self, candidate: tuple[int, int], grid: list[str]) -> bool:
        """Check if the candidate valid.

        Args:
        ----
            candidate: The candidate to check.
            grid: The grid to check.

        Returns:
        -------
            True if the candidate is valid.

        """
        x, y = candidate
        diagonal_1 = grid[x - 1][y - 1] + grid[x][y] + grid[x + 1][y + 1]
        diagonal_2 = grid[x - 1][y + 1] + grid[x][y] + grid[x + 1][y - 1]
        return (diagonal_1 == "MAS" or diagonal_1 == "SAM") and (
            diagonal_2 == "MAS" or diagonal_2 == "SAM"
        )

    def count_target_words(self) -> int:
        """Count the target words in the grid."""
        # Find candidates for the target word (center character being
        # "A")
        candidates: list[tuple[int, int]] = []
        for x, line in enumerate(self.grid):
            if x == 0 or x == len(self.grid) - 1:
                continue
            for y, char in enumerate(line):
                if y == 0 or y == len(line) - 1:
                    continue
                if char == "A":
                    candidates.append((x, y))
        return sum([self.is_x_mas(candidate, self.grid) for candidate in candidates])


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    return WordSearch(input_lines).count_target_words()


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    return XMasWordSearch(input_lines).count_target_words()


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_4.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
