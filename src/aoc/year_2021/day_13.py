# https://adventofcode.com/2021/day/13

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class Position:
    x: int
    y: int


class Direction(Enum):
    x = "x"
    y = "y"


@dataclass()
class Fold:
    position: int
    direction: Direction


class TransparentPaper:
    """Represents a single piece of transparent paper that can be
    folded.

    Args:
        dots (list[Position]): List of positions of dots on this piece
            of paper.
    """

    def __init__(self, dots: list[Position]) -> None:
        self.dots: list[Position] = dots

        # Create a grid and plot all the dots on the grid as 1
        max_x = max(dot.x for dot in self.dots) + 1
        max_y = max(dot.y for dot in self.dots) + 1
        self._grid = np.zeros((max_y, max_x))
        for dot in self.dots:
            self._grid[dot.y, dot.x] = 1

    def to_string(self) -> str:
        """Convert the grid to a string so the final output can be read.

        Returns:
            str: The folded paper as a string.
        """

        output: list[str] = []
        for y in range(self._grid.shape[0]):
            line: list[str] = []
            for x in range(self._grid.shape[1]):
                line.append("#" if self._grid[y, x] == 1 else ".")
            output.append("".join(line))
        return "\n".join(output)

    @property
    def n_visible_dots(self) -> int:
        """Count the number of positions that contain a dot."""
        return (self._grid == 1).sum()

    def fold(self, fold: Fold):
        """Fold this piece of paper.

        Args:
            fold (Fold): The type of fold and the position to fold.
        """

        # Fold horizontally
        if fold.direction == Direction.x:
            left = self._grid[:, : fold.position]
            right = np.flip(self._grid[:, fold.position + 1 :], axis=1)

            # Overlay left and right
            self._grid = (left + right).clip(max=1)

        # Fold vertically
        else:
            top = self._grid[: fold.position]
            bottom = np.flip(self._grid[fold.position + 1 :], axis=0)

            # Overlay top and bottom
            self._grid = (top + bottom).clip(max=1)

    @classmethod
    def from_text(self, input_lines: list[str]) -> TransparentPaper:
        """Create a piece of paper from dot definitions.

        Args:
            input_lines (list[str]): The dots on the paper as X, Y
                positions.

        Returns:
            TransparentPaper: The parsed paper.
        """

        positions: list[Position] = []
        for line in input_lines:
            x, y = line.split(",")
            positions.append(Position(x=int(x), y=int(y)))
        return TransparentPaper(dots=positions)


def parse_input(input_lines: list[str]) -> tuple[TransparentPaper, list[Fold]]:
    dots = [line for line in input_lines if not line.startswith("fold along")]
    folds_text = [
        line.lstrip("fold along ")
        for line in input_lines
        if line.startswith("fold along")
    ]
    folds: list[Fold] = []
    for fold_text in folds_text:
        direction, value = fold_text.split("=")
        folds.append(Fold(position=int(value), direction=Direction[direction]))

    paper = TransparentPaper.from_text(dots)

    return paper, folds


def part_one(input_lines: list[str]) -> int:

    # Parse the input
    paper, folds = parse_input(input_lines)

    # Make only the first fold
    paper.fold(folds[0])

    return paper.n_visible_dots


def part_two(input_lines: list[str]) -> str:

    # Parse the input
    paper, folds = parse_input(input_lines)

    # Make all the folds
    for fold in folds:
        paper.fold(fold)

    # Return the folded paper as a string
    return paper.to_string()


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_13.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines() if line.strip() != ""]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result_two = part_two(input_lines)
    print("Part two:", f"\n{result_two}")
