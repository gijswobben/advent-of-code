# https://adventofcode.com/2022/day/23

from __future__ import annotations

import functools
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class Position:
    x: int
    y: int


class RelativePosition(Enum):
    NW = Position(-1, -1)
    N = Position(0, -1)
    NE = Position(1, -1)
    E = Position(1, 0)
    SE = Position(1, 1)
    S = Position(0, 1)
    SW = Position(-1, 1)
    W = Position(-1, 0)

    @functools.lru_cache(maxsize=None)
    def to_absolute(self, position: Position) -> Position:
        """Convert this relative position in an absolute position give a
        certain position.

        Args:
            position (Position): The position to start from.

        Returns:
            Position: The position after applying the relative position.
        """
        return Position(x=position.x + self.value.x, y=position.y + self.value.y)


class Elf:
    """Representation of a single Elf.

    Args:
        position (Position): The starting position of this Elf.
    """

    def __init__(self, position: Position) -> None:
        self.position = position
        self.considered_position: Position | None = None
        self.consideration_order: list[Callable[[], Position | None]] = [
            self._consider_north,
            self._consider_south,
            self._consider_west,
            self._consider_east,
        ]

    def _consider_orientation(
        self, relative_positions: list[RelativePosition]
    ) -> Position | None:
        if all(
            [
                self._elves_at[relative_position] is None
                for relative_position in relative_positions
            ]
        ):
            return relative_positions[1].to_absolute(self.position)
        else:
            return None

    def _consider_north(self) -> Position | None:
        return self._consider_orientation(
            relative_positions=[
                RelativePosition.NW,
                RelativePosition.N,
                RelativePosition.NE,
            ],
        )

    def _consider_south(self) -> Position | None:
        return self._consider_orientation(
            relative_positions=[
                RelativePosition.SW,
                RelativePosition.S,
                RelativePosition.SE,
            ],
        )

    def _consider_west(self) -> Position | None:
        return self._consider_orientation(
            relative_positions=[
                RelativePosition.NW,
                RelativePosition.W,
                RelativePosition.SW,
            ],
        )

    def _consider_east(self) -> Position | None:
        return self._consider_orientation(
            relative_positions=[
                RelativePosition.NE,
                RelativePosition.E,
                RelativePosition.SE,
            ],
        )

    def consider_next_position(self, on: Ground) -> None:
        """Consider the next position for this elf.

        Args:
            on (Ground): The ground to move on.
        """

        # Store elves at relative positions
        self._elves_at: dict[RelativePosition, Elf | None] = {
            relative_position: on.get_elf_at_position(
                relative_position.to_absolute(self.position)
            )
            for relative_position in RelativePosition
        }

        # Elf won't move if there are no other elves around
        if all([elf is None for elf in self._elves_at.values()]):
            self.considered_position = None

        else:
            self.considered_position = None
            for consider in self.consideration_order:
                position = consider()
                if position is not None:
                    self.considered_position = position
                    break

    def move(self, on: Ground) -> bool:
        """Move the elf if possible.

        Args:
            on (Ground): The ground to move on.

        Returns:
            bool: Whether or not the elf moved.
        """

        # Make sure the elf considered a next position
        if (
            self.considered_position is not None
            and self.considered_position != self.position
        ):
            # Check if any other elves considered the same location to move
            # to
            if not any(
                [
                    elf.considered_position == self.considered_position
                    for elf in on.elves
                    if elf != self
                ]
            ):
                self.position = self.considered_position
                return True

        return False


class Ground:
    """Representation of the full grounds."""

    def __init__(self, elves: list[Elf]) -> None:
        self.elves = elves

    @property
    def smallest_rectangle(self) -> np.ndarray:
        """The smallest rectangle that captures all elves.

        Returns:
            np.ndarray: An array with 0 for empty tiles and 1 for tiles that contain an elf.
        """

        # Get the boundaries of the rectangle
        left = min([elf.position.x for elf in self.elves])
        right = max([elf.position.x for elf in self.elves]) + 1
        top = min([elf.position.y for elf in self.elves])
        bottom = max([elf.position.y for elf in self.elves]) + 1
        width = right - left
        height = bottom - top

        # Create an empty grid according to the boundaries of the
        # rectangle and place the elves on the grid
        rectangle = np.zeros((height, width))
        for elf in self.elves:
            rectangle[elf.position.y - top, elf.position.x - left] = 1
        return rectangle

    @functools.lru_cache(maxsize=None)
    def get_elf_at_position(self, position: Position) -> Elf | None:
        """Get an elf by postion, if there is one.

        Args:
            position (Position): Position to look at.

        Returns:
            Elf | None: The elf, or None if no elf is at this position.
        """
        return next((elf for elf in self.elves if elf.position == position), None)

    def simulate(self, rounds: int = sys.maxsize) -> int:
        """Simulate N rounds of moving elves.

        Args:
            rounds (int, optional): The number of rounds to run. Will
                stop automatically if no elves moved during the last
                round. Defaults to sys.maxsize.

        Returns:
            int: The last round.
        """

        for round in range(rounds):
            print(round + 1)

            # First half
            for elf in self.elves:
                elf.consider_next_position(on=self)

            # Second half
            moved: list[bool] = [elf.move(on=self) for elf in self.elves]
            if not any(moved):
                break

            # Change the order of considering directions
            for elf in self.elves:
                elf.consideration_order.append(elf.consideration_order.pop(0))

            # Clear cache
            self.get_elf_at_position.cache_clear()

        return round + 1

    def print(self) -> None:
        """Print the grid in a similar fashion as the examples."""

        smallest_rectangle = self.smallest_rectangle
        lines: list[str] = []
        for y in range(smallest_rectangle.shape[0]):
            line: list[str] = []
            for x in range(smallest_rectangle.shape[1]):
                line.append("#" if smallest_rectangle[y, x] == 1 else ".")
            lines.append("".join(line))
        print("\n".join(lines))

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Ground:
        """Parse the ground from text."""

        elves: list[Elf] = []
        for y, line in enumerate(input_lines):
            for x, character in enumerate(line):
                if character == "#":
                    elves.append(Elf(Position(x=x, y=y)))
        return Ground(elves=elves)


def part_one(input_lines: list[str]) -> int:

    # Parse the input
    ground = Ground.from_text(input_lines=input_lines)

    # Simulate for 10 rounds
    ground.simulate(rounds=10)

    # Count the number of tiles that are 0 (empty)
    empty_tiles = np.count_nonzero(ground.smallest_rectangle == 0)
    return empty_tiles


def part_two(input_lines: list[str]) -> int:

    # Parse the input
    ground = Ground.from_text(input_lines=input_lines)

    # Keep simulating until no elves move, get the round number
    round = ground.simulate()
    return round


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_23.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
