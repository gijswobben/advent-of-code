# https://adventofcode.com/2022/day/9

from __future__ import annotations

from enum import Enum
from pathlib import Path


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Knot:
    """Class that represents a single knot in a rope.

    Args:
        initial_x (int, optional): The starting position. Defaults to 0.
        initial_y (int, optional): The starting position. Defaults to 0.
        following (Knot | None, optional): The knot that this knot is
            following (if any). Defaults to None.
    """

    def __init__(
        self, initial_x: int = 0, initial_y: int = 0, following: Knot | None = None
    ) -> None:
        self.x = initial_x
        self.y = initial_y
        self.following = following
        self._visited: list[tuple[int, int]] = [(0, 0)]

    @property
    def positions_visited(self) -> int:
        """Number of (unique) visited positions."""
        return len(set(self._visited))

    def follow(self) -> None:
        """Move this knot to keep following the knot it is following (if
        any).
        """

        # Skip if this knot is the last
        if self.following is None:
            return

        # Calculate the relative position to the knot that is being
        # followed
        relative_position = (self.following.x - self.x, self.following.y - self.y)

        # Mapping between relative position and desired movement of this
        # knot
        relative_positions: dict[tuple[int, int], tuple[int, int]] = {
            (-2, -1): (-1, -1),
            (-2, 0): (-1, 0),
            (-2, 1): (-1, 1),
            (2, -1): (1, -1),
            (2, 0): (1, 0),
            (2, 1): (1, 1),
            (-1, -2): (-1, -1),
            (0, -2): (0, -1),
            (1, -2): (1, -1),
            (-1, 2): (-1, 1),
            (0, 2): (0, 1),
            (1, 2): (1, 1),
            (-2, -2): (-1, -1),
            (2, -2): (1, -1),
            (2, 2): (1, 1),
            (-2, 2): (-1, 1),
        }

        # Get the desired relative position and move this knot
        movement = relative_positions.get(relative_position, (0, 0))
        self.x += movement[0]
        self.y += movement[1]

        # Add the new position to the list of visited positions
        self._visited.append((self.x, self.y))


class Rope:
    """Class that represents a re rope (combination of knots).

    Args:
        length (int): The total length (number of knots) in the rope,
            including the head. Defaults to 2.
    """

    def __init__(self, length: int = 2) -> None:
        self.knots = [Knot(0, 0)]
        for _ in range(length - 1):
            self.knots.append(Knot(0, 0, self.knots[-1]))

    def move(self, direction: Direction, units: int):
        """Move the head of the rope for N units in a particular
        direction.

        Args:
            direction (Direction): The direction to move in.
            units (int): The number of units to move the head.
        """
        for _ in range(units):
            # Move the head
            self.knots[0].x += direction.value[0]
            self.knots[0].y += direction.value[1]

            # Update the rest of the knots
            for knot in self.knots[1:]:
                knot.follow()


def part_one(input_lines: list[str]) -> int:

    # Create a rope with 2 knots (head and tail)
    rope = Rope(length=2)

    # Loop all the instructions
    for line in input_lines:
        direction_string, units_string = line.split(" ")
        units = int(units_string)
        if direction_string == "R":
            direction = Direction.RIGHT
        elif direction_string == "L":
            direction = Direction.LEFT
        elif direction_string == "U":
            direction = Direction.UP
        elif direction_string == "D":
            direction = Direction.DOWN
        else:
            raise

        # Move the rope
        rope.move(direction, units=units)

    # Get the number of visited positions of the last knot in the rope
    return rope.knots[-1].positions_visited


def part_two(input_lines: list[str]) -> int:

    # Create a rope with 10 knots (1 head + 9 knots)
    rope = Rope(length=10)

    # Loop all the instructions
    for line in input_lines:
        direction_string, units_string = line.split(" ")
        units = int(units_string)
        if direction_string == "R":
            direction = Direction.RIGHT
        elif direction_string == "L":
            direction = Direction.LEFT
        elif direction_string == "U":
            direction = Direction.UP
        elif direction_string == "D":
            direction = Direction.DOWN
        else:
            raise

        # Move the rope
        rope.move(direction, units=units)

    # Get the number of visited positions of the last knot in the rope
    return rope.knots[-1].positions_visited


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_9.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
