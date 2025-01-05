# https://adventofcode.com/2022/day/24

from __future__ import annotations

import functools
import math
from collections import deque
from dataclasses import dataclass
from enum import Enum, IntEnum
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cityblock


@dataclass(frozen=True)
class Position:
    """Represents a position in the valley."""

    x: int
    y: int

    def is_valid(self, on: np.ndarray) -> bool:
        """Determine if this is a valid position on a specific grid.

        A position is valid if it is on the grid and the position is
        empty.

        Args:
            on (np.ndarray): The grid to determine valid moves on.

        Returns:
            bool: Whether or not the position is a valid move.
        """

        if self.x < 0 or self.x >= on.shape[1] or self.y < 0 or self.y >= on.shape[0]:
            return False
        else:
            return on[self.y, self.x] == Tile.EMPTY


class Direction(Enum):
    """All relative positions that can be moved to (including the
    current position)."""

    LEFT = Position(x=-1, y=0)
    TOP = Position(x=0, y=-1)
    RIGHT = Position(x=1, y=0)
    BOTTOM = Position(x=0, y=1)
    STAY = Position(x=0, y=0)


class Tile(IntEnum):
    """Possible contents of each tile in the valley."""

    EMPTY = 0
    BLIZZARD = 1
    TEAM = 2
    WALL = 8


class Valley:
    """Represents a valley in which different blizzards move.

    Args:
        width (int): Width of the valley.
        height (int): height of the valley.
        entrance (Position): Position where the entrance to the valley
            is.
        exit (Position): Position where the exit of the valley is.
        blizzards (list[Blizzard]): List of blizzards that are in the
            valley.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entrance: Position,
        exit: Position,
        blizzards: list[Blizzard],
    ) -> None:
        self.entrance = entrance
        self.exit = exit
        self.blizzards = blizzards
        self.width = width
        self.height = height

        # Create the walls by padding with "wall"
        self._grid = np.pad(
            np.zeros((self.height - 2, self.width - 2)), (1,), constant_values=Tile.WALL
        )

        # Clear the entrance and exit positions
        self._grid[self.entrance.y, self.entrance.x] = Tile.EMPTY
        self._grid[self.exit.y, self.exit.x] = Tile.EMPTY

    @functools.lru_cache(maxsize=None)
    def distance_to_entrance(self, position: Position) -> int:
        """Manhattan distance from a position to the entrance."""

        return cityblock(position, self.entrance)

    @functools.lru_cache(maxsize=None)
    def distance_to_exit(self, position: Position) -> int:
        """Manhattan distance from a position to the exit."""

        return cityblock(position, self.exit)

    def traverse(
        self,
        start: Position | None = None,
        finish: Position | None = None,
        time: int = 0,
    ) -> int:
        """Move from start to finish in the shortest way possible and
        return the time it takes.

        Path is determined using a Breadth First Search (BFS).

        Args:
            start (Position | None, optional): The starting position.
                Defaults to the valley entrance.
            finish (Position | None, optional): The finish position.
                Defaults to the valley exit.
            time (int, optional): The initial time. Defaults to 0.

        Returns:
            int: The elapsed time to get to the finish.
        """

        # If the starting point or exit is not defined, use entrance and
        # exit as defaults
        if start is None:
            start = self.entrance
        if finish is None:
            finish = self.exit

        # Add the start node
        queue = deque([start])

        # Precompute all blizzard states
        blizzard_states = self._get_all_blizzard_states()
        n_states = len(blizzard_states.keys())

        # Keep going until the queue is empty, or the exit is found
        while queue:
            time += 1
            seen: set[Position] = set()

            # Loop the current queue items
            for _ in range(len(queue)):
                position = queue.popleft()

                # Stop if the next item is the exit
                if position == finish:
                    return time - 1

                # List valid neighbours for this element
                neighbours: list[Position] = [
                    Position(
                        x=position.x + direction.value.x,
                        y=position.y + direction.value.y,
                    )
                    for direction in Direction
                ]

                # Filter the neighbours to valid moves in this
                # blizzard state
                neighbours = [
                    neighbour
                    for neighbour in neighbours
                    if 0 <= neighbour.x < self.width
                    and 0 <= neighbour.y < self.height
                    and blizzard_states[time % n_states][neighbour.y, neighbour.x]
                    == Tile.EMPTY
                ]

                # Add the neighbours to the queue
                for neighbour in neighbours:
                    if neighbour not in seen:
                        seen.add(neighbour)
                        queue.append(neighbour)

        # Return the time it takes to get to the target
        return time

    def _get_all_blizzard_states(self) -> dict[int, np.ndarray]:
        """Precompute all blizzard states.

        Because the blizzards move in a predictable pattern that repeats
        every Least Combined Multiplier (LCM) of the width and height of
        the valley (excluding walls), all the possible blizzard
        states/configurations can be precomputed for speed.

        Returns:
            dict[int, np.ndarray]: The precomputed blizzard states.
        """

        # Possible number of states is the Least Combined Multiplier
        # (LCM) of width and height
        n_states = math.lcm(self.width - 2, self.height - 2) - 1

        # Initial state is at t = 0
        states: dict[int, np.ndarray] = {0: self.plot_on_grid()}

        # Generate all states
        for state in range(1, n_states + 1):

            # Move blizzards relative to the previous state
            for blizzard in self.blizzards:
                blizzard.move(on=states[state - 1])
            states[state] = self.plot_on_grid()

        return states

    def plot_on_grid(self) -> np.ndarray:
        """Put the blizzard objects in their current state on a grid.

        Returns:
            np.ndarray: The grid with blizzards.
        """

        # Make a copy of the grid
        grid = self._grid.copy()

        # Loop all blizzards and set their positions
        for blizzard in self.blizzards:
            grid[blizzard.position.y, blizzard.position.x] = Tile.BLIZZARD
        return grid

    def to_string(self) -> str:
        """Helper method to get the same string representation of a grid
        as in the examples.

        Debugging purposes.

        Returns:
            str: The grid as a string.
        """
        grid = self.plot_on_grid()
        mapping: dict[Tile, str] = {
            Tile.EMPTY: ".",
            Tile.BLIZZARD: "+",
            Tile.TEAM: "E",
            Tile.WALL: "#",
        }
        lines: list[str] = []
        for y in range(grid.shape[0]):
            line: list[str] = []
            for x in range(grid.shape[1]):
                line.append(mapping[grid[y, x]])
            lines.append("".join(line))
        return "\n".join(lines)

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Valley:
        """Create a Valley object from a list of strings.

        Args:
            input_lines (list[str]): Current state of the valley as a
                list of strings (one string per row).

        Raises:
            Exception: Raised when an invalid input is encountered.

        Returns:
            Valley: The parsed valley object.
        """

        width = len(input_lines[0])
        height = len(input_lines)

        # Determine entrance and exit positions
        entrance = Position(x=input_lines[0].index("."), y=0)
        exit = Position(x=input_lines[-1].index("."), y=height - 1)

        blizzards: list[Blizzard] = []
        for y, line in enumerate(input_lines[1:-1], start=1):
            for x, character in enumerate(line[1:-1], start=1):

                # Not a blizzard
                if character == ".":
                    continue

                # Get the direction of the blizzard
                direction = {
                    "<": Direction.LEFT,
                    ">": Direction.RIGHT,
                    "^": Direction.TOP,
                    "v": Direction.BOTTOM,
                }.get(character)
                if direction is None:
                    raise Exception(f"Invalid character {character}")

                # Add to the list
                blizzards.append(Blizzard(direction=direction, position=Position(x, y)))

        return Valley(
            width=width,
            height=height,
            entrance=entrance,
            exit=exit,
            blizzards=blizzards,
        )


class Blizzard:
    """Represents a single blizzard.

    Args:
        direction (Direction): The direction this blizzard is facing.
        position (Position): The position of this blizzard in the
            valley.
    """

    def __init__(self, direction: Direction, position: Position) -> None:
        self.direction = direction
        self.position = position

    def move(self, on: np.ndarray):
        """Move this blizzard in the valley.

        Args:
            on (np.ndarray): The valley to move in.
        """

        # Determine the next position this blizzard will be in
        next_position = Position(
            x=self.position.x + self.direction.value.x,
            y=self.position.y + self.direction.value.y,
        )

        # If that position is a wall, wrap around the valley
        if on[next_position.y, next_position.x] == Tile.WALL:
            if self.direction == Direction.LEFT:
                next_position = Position(x=on.shape[1] - 2, y=self.position.y)
            elif self.direction == Direction.RIGHT:
                next_position = Position(x=1, y=self.position.y)
            elif self.direction == Direction.TOP:
                next_position = Position(x=self.position.x, y=on.shape[0] - 2)
            elif self.direction == Direction.BOTTOM:
                next_position = Position(x=self.position.x, y=1)

        # Move the blizzard
        self.position = next_position


def part_one(input_lines: list[str]) -> int:

    # Create the valley from the input
    valley = Valley.from_text(input_lines=input_lines)

    # Move through the valley and return the time it takes
    time = valley.traverse(start=valley.entrance, finish=valley.exit)
    return time


def part_two(input_lines: list[str]) -> int:

    # Create the valley from the input
    valley = Valley.from_text(input_lines=input_lines)

    # Move from start to finish multiple times
    time = 0
    legs: list[tuple[Position, Position]] = [
        (valley.entrance, valley.exit),
        (valley.exit, valley.entrance),
        (valley.entrance, valley.exit),
    ]
    for start, finish in legs:
        time = valley.traverse(start=start, finish=finish, time=time)

    # Minus 1 for every "turnaround"
    return time - (len(legs) - 1)


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_24.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
