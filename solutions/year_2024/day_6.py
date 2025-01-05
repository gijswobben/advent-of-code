"""Assignment for day 6 of 2024 Advent of Code.

https://adventofcode.com/2024/day/6
"""

from __future__ import annotations

from collections import namedtuple
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, computed_field
from rich import print
from tqdm import tqdm


class Direction(StrEnum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"
    MISSING = "X"


Position = namedtuple("Position", ["x", "y", "direction"])


class Map(BaseModel):
    width: int
    height: int
    obstacles: list[Position]


class Guard(BaseModel):
    x: int
    y: int
    direction: Direction
    path: list[Position] = Field(default_factory=list)

    @computed_field
    @property
    def current_position(self) -> Position:
        return Position(x=self.x, y=self.y, direction=self.direction)


class SimulationResult(StrEnum):
    OUT_OF_BOUNDS = "out_of_bounds"
    SELF_LOOP = "self_loop"


next_direction_lookup: dict[Direction, Direction] = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

character_mapping: dict[str, int] = {
    ".": 0,
    "#": -1,
    **{direction.value: 1 for direction in Direction},
}


class Lab:
    def __init__(self, input_lines: list[str]) -> None:
        # Store the input lines
        self.input_lines = input_lines

        # Parse the input lines to determine the starting position and
        # obstacles
        self.starting_obstacles: list[Position] = []
        for y, line in enumerate(input_lines):
            for x, char in enumerate(line):
                if char == ".":
                    continue
                elif char == "#":
                    self.starting_obstacles.append(
                        Position(x=x, y=y, direction=Direction.MISSING),
                    )
                else:
                    self.starting_position = Position(
                        x=x,
                        y=y,
                        direction=Direction(char),
                    )

    def reset(self, additional_obstacles: list[Position] | None) -> None:
        additional_obstacles = (
            additional_obstacles if additional_obstacles is not None else []
        )
        # Create the map
        self.map = Map(
            width=len(self.input_lines[0]),
            height=len(self.input_lines),
            obstacles=self.starting_obstacles + additional_obstacles,
        )

        # Place the guard at the starting position
        self.guard = Guard(
            x=self.starting_position.x,
            y=self.starting_position.y,
            direction=self.starting_position.direction,
            path=[self.starting_position],
        )

    def _next_guard_position(self) -> tuple[int, int]:
        if self.guard.direction == Direction.UP:
            return (self.guard.x, self.guard.y - 1)
        elif self.guard.direction == Direction.DOWN:
            return (self.guard.x, self.guard.y + 1)
        elif self.guard.direction == Direction.LEFT:
            return (self.guard.x - 1, self.guard.y)
        elif self.guard.direction == Direction.RIGHT:
            return (self.guard.x + 1, self.guard.y)
        else:
            raise ValueError("Invalid direction")

    def simulate_guard(
        self,
        additional_obstacles: list[Position] | None = None,
    ) -> SimulationResult:
        # Start with a clean simulation environment
        self.reset(additional_obstacles=additional_obstacles)

        # Simulate the guard moving
        while True:
            # Get the next position of the guard
            next_x, next_y = self._next_guard_position()

            # If the guard is out of bounds, stop the simulation
            if (
                next_x < 0
                or next_x >= self.map.width
                or next_y < 0
                or next_y >= self.map.height
            ):
                return SimulationResult.OUT_OF_BOUNDS

            # If the guard returns to a position it has already visited,
            # stop the simulation
            elif (
                Position(x=next_x, y=next_y, direction=self.guard.direction)
                in self.guard.path
            ):
                return SimulationResult.SELF_LOOP

            # If the position is blocked, turn right
            if (
                Position(x=next_x, y=next_y, direction=Direction.MISSING)
                in self.map.obstacles
            ):
                self.guard.direction = next_direction_lookup[self.guard.direction]
                self.guard.path.append(self.guard.current_position)

            # If the position is not blocked, move the guard
            else:
                self.guard.x = next_x
                self.guard.y = next_y
                self.guard.path.append(self.guard.current_position)

    def detect_obstacle_options(self) -> int:
        # The obstacle has to be placed in the current path of the
        # guard, so simulate the movement of the guard to determine
        # the valid positions
        self.simulate_guard()
        candidates: list[Position] = self.unique_positions_taken

        # Loop the candicates and check if they are valid, meaning they
        # cause the guard to move in a loop. Skip the first position
        # because it is the starting position of the guard
        valid_obstacles: list[Position] = []
        for candidate in candidates[1:]:
            if (
                self.simulate_guard(additional_obstacles=[candidate])
                == SimulationResult.SELF_LOOP
            ):
                valid_obstacles.append(candidate)

        return len(valid_obstacles)

    @property
    def unique_positions_taken(self) -> list[Position]:
        unique_positions: list[tuple[int, int]] = []
        for position in self.guard.path:
            if (position.x, position.y) not in unique_positions:
                unique_positions.append((position.x, position.y))
        return [
            Position(x=x, y=y, direction=Direction.MISSING) for x, y in unique_positions
        ]


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    # Create the lab
    lab = Lab(input_lines)

    # Simulate the guard
    lab.simulate_guard()

    # Return the number of unique positions taken by the guard
    return len(lab.unique_positions_taken)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    # Create the lab
    lab = Lab(input_lines)

    # Detect the number of valid obstacle options
    return lab.detect_obstacle_options()


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_6.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
