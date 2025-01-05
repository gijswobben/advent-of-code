# https://adventofcode.com/2022/day/14

from __future__ import annotations

import itertools
from pathlib import Path
from typing import cast

import numpy as np


class Cave:
    """Model of the cave with rock formations and sand.

    Args:
        width (int): The (minimum) width of the cave.
        height (int): The height of the cave.
        rocks (list[tuple[tuple[int, int], tuple[int, int]]]): The rock
            formations as a list of source and target coordinates.
        source_position (tuple[int, int]): The position (coordinates) of
            the source that produces new sand. Defaults to (500, 0).
    """

    def __init__(
        self,
        width: int,
        height: int,
        rocks: list[tuple[tuple[int, int], tuple[int, int]]],
        source_position: tuple[int, int] = (500, 0),
    ) -> None:
        self.ticks = 0  # Ticks on the clock
        self.source_position = source_position

        # Create a grid of zeroes (empty positions) at least twice the
        # minimum width. Add 1 to the height. This extra row will be
        # used to check for "overflow".
        self.grid = np.zeros((height + 2, width * 2 + 1))

        # Draw the rocks on the grid (set cells to 1)
        self.draw_rocks(rocks=rocks)

    def tick(self) -> bool:
        """Progress time by 1 unit.

        Every unit a new grain of sand enters/falls into the cave.

        Returns:
            bool: Whether or not the cave "overflowed".
        """

        # Create a new grain of sand and have it fall
        new_grain = Grain(
            x=self.source_position[0], y=self.source_position[1], cave=self
        )
        new_grain.fall()

        # Stop if it sits on the source position (unable to move)
        if (new_grain.x, new_grain.y) == self.source_position:
            return True

        # Draw the grain on the grid
        self.grid[new_grain.y, new_grain.x] = 2

        # Test if the bottom layer is empty (while not being the floor)
        if not all(self.grid[-1, :] == 0) and not all(self.grid[-1, :] == 1):
            return True

        # Increase the clock ticks
        self.ticks += 1
        return False

    def draw_rocks(self, rocks: list[tuple[tuple[int, int], tuple[int, int]]]):
        """Draw a line of rocks in the cave.

        A line of rocks is defined by a starting point (x, y) and an end
        point (x, y). All rock formations have to be horizontal or
        vertical.

        Args:
            rocks (list[tuple[tuple[int, int], tuple[int, int]]]): List
                of start and end tuples.

        Raises:
            Exception: Raised when a diagonal rock formation is given.
        """
        for rock_source, rock_target in rocks:

            # Vertical line
            if rock_source[0] == rock_target[0]:
                top = min(rock_source[1], rock_target[1])
                bottom = max(rock_source[1], rock_target[1])
                for vertical_position in range(top, bottom + 1):
                    self.grid[vertical_position, rock_source[0]] = 1

            # Horizontal line
            elif rock_source[1] == rock_target[1]:
                left = min(rock_source[0], rock_target[0])
                right = max(rock_source[0], rock_target[0])
                for horizontal_position in range(left, right + 1):
                    self.grid[rock_source[1], horizontal_position] = 1

            else:
                raise Exception("Invalid rock formation")

    @classmethod
    def from_text(
        cls,
        input_lines: list[str],
    ) -> Cave:
        """Create a new cave from the input lines.

        Args:
            input_lines (list[str]): Line by line description of rock
                formations.

        Returns:
            Cave: The resulting cave.
        """
        max_x: int = 0
        max_y: int = 0
        rocks: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for line in input_lines:
            points = [
                tuple(int(el) for el in point.split(",", maxsplit=1))
                for point in line.split(" -> ")
            ]
            for source, target in itertools.pairwise(points):
                max_x = max(source[0], target[0], max_x)
                max_y = max(source[1], target[1], max_y)
                rocks.append(
                    cast(tuple[tuple[int, int], tuple[int, int]], (source, target))
                )

        return Cave(width=max_x, height=max_y, rocks=rocks)


class Grain:
    """Represents a single grain of sand.

    Args:
        x (int): The horizontal position of the grain.
        y (int): The vertical position of the grain.
        cave (Cave): The cave that this grain is in.
    """

    def __init__(self, x: int, y: int, cave: Cave):
        self.x = x
        self.y = y
        self.cave = cave

    def fall(self):
        """Let the grain "fall" into the cave from its starting point.

        The grain will keep on moving until it settles in a place where
        no more movement is possible.
        """

        # Keep falling until it has nowhere to go
        while True:

            # Check next position down
            if (
                self.y + 1 < self.cave.grid.shape[0]
                and self.cave.grid[self.y + 1, self.x] == 0
            ):
                self.y += 1

            # Side left
            elif (
                self.y + 1 < self.cave.grid.shape[0]
                and self.x - 1 > 0
                and self.cave.grid[self.y + 1, self.x - 1] == 0
            ):
                self.y += 1
                self.x -= 1

            # Side right
            elif (
                self.y + 1 < self.cave.grid.shape[0]
                and self.x + 1 < self.cave.grid.shape[1]
                and self.cave.grid[self.y + 1, self.x + 1] == 0
            ):
                self.y += 1
                self.x += 1

            # Unable to move so stop falling
            else:
                break

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<x={self.x}, y={self.y}>"


def part_one(input_lines: list[str]) -> int:

    # Create a representation of the cave for the input
    cave = Cave.from_text(input_lines)

    # Keep running until it overflows (either no more room to add new
    # grains or grains folling through)
    while True:
        did_overflow = cave.tick()
        if did_overflow:
            break

    # Return the time (ticks) when the cave overflows
    return cave.ticks


def part_two(input_lines: list[str]) -> int:

    # Create a representation of the cave for the input
    cave = Cave.from_text(input_lines)

    # Create the floor by extending the vertical space by 1 and add the
    # floor as a large piece of rock at the bottom
    cave.grid = np.pad(cave.grid, (0, 1))
    cave.draw_rocks(
        rocks=[
            (
                (
                    (0, cave.grid.shape[0] - 1),
                    (cave.grid.shape[1] - 1, cave.grid.shape[0] - 1),
                )
            )
        ]
    )

    # Keep running until it overflows (either no more room to add new
    # grains or grains folling through)
    while True:
        did_overflow = cave.tick()
        if did_overflow:
            break

    # Return the time (ticks) when the cave overflows
    return cave.ticks + 1


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_14.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
