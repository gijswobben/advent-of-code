# https://adventofcode.com/2022/day/18

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

import numpy as np


class Content(IntEnum):
    AIR = 0
    LAVA = 1


@dataclass(frozen=True)
class Position:
    """Represents a 3D position in the lava."""

    x: int
    y: int
    z: int


class Lava:
    """Represents the lava blob as a 3D grid.

    Args:
        dimension_x (int): The grid size in the X direction.
        dimension_y (int): The grid size in the Y direction.
        dimension_z (int): The grid size in the Z direction.
        points (list[Position]): List of positions where lava is.
    """

    def __init__(
        self,
        dimension_x: int,
        dimension_y: int,
        dimension_z: int,
        points: list[Position],
    ) -> None:

        # Create an empty 3D grid and mark lava as 1
        self._grid = np.zeros((dimension_x, dimension_y, dimension_z))
        for point in points:
            self._grid[point.x, point.y, point.z] = Content.LAVA

    def contact_surface(self, without_pockets: bool = False) -> int:

        # Make a copy of the grid to work on
        grid = self._grid.copy()

        # All directions to inspect (relative to each cube in the grid)
        relative_positions: list[Position] = [
            Position(-1, 0, 0),
            Position(1, 0, 0),
            Position(0, -1, 0),
            Position(0, 1, 0),
            Position(0, 0, -1),
            Position(0, 0, 1),
        ]

        def _get_pocket(
            position: Position, pocket: list[Position] | None = None
        ) -> list[Position]:
            # Recursively expand the well, return full set if the
            # well doesn't breaks into the open

            # Skip any cubes at the edge
            if (
                position.x <= 0
                or position.x >= grid.shape[0]
                or position.y <= 0
                or position.y >= grid.shape[1]
                or position.z <= 0
                or position.z >= grid.shape[2]
            ):
                raise IndexError("Invalid")

            # Consider this position part of a pocket
            if pocket is None:
                pocket = []
            pocket.append(position)

            # Look in all directions
            neighbours = [
                Position(
                    relative.x + position.x,
                    relative.y + position.y,
                    relative.z + position.z,
                )
                for relative in relative_positions
            ]

            # Filter to only neighbours that are empty and not in the
            # pocket already
            neighbours = [
                neighbour
                for neighbour in neighbours
                if grid[neighbour.x, neighbour.y, neighbour.z] == Content.AIR
                and neighbour not in pocket
            ]

            # Check all the neighbours
            for neighbour in neighbours:
                neighbour_well = _get_pocket(neighbour, pocket=pocket)
                pocket.extend(neighbour_well)

            # Return only unique positions
            return list(set(pocket))

        # If pockets of "air" should be excluded, fill in all pockets
        # with lava so it doesn't have any contact surface anymore
        if without_pockets:

            # Determine if a pocket exists by "growing" each cube in all
            # directions
            for x, y, z in np.ndindex(grid.shape):

                # Go over empty cubes ("air") only
                if grid[x, y, z] == Content.AIR:

                    # If this is a pocket, close it by setting all
                    # positions in the pocket to LAVA
                    try:
                        pocket = _get_pocket(position=Position(x, y, z))
                        if pocket is not None:
                            for cell in pocket:
                                grid[cell.x, cell.y, cell.z] = Content.LAVA
                    except IndexError:
                        # Not a pocket
                        pass

        # For every position in the grid count the total contact area
        total = 0
        for x, y, z in np.ndindex(grid.shape):

            if grid[x, y, z] == Content.LAVA:

                # Check all sides of the "cube"
                for relative in relative_positions:
                    try:
                        if (
                            grid[relative.x + x, relative.y + y, relative.z + z]
                            == Content.AIR
                        ):
                            total += 1
                    except Exception:
                        total += 1

        return total

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Lava:
        """Parse the input text as a Lava object.

        Args:
            input_lines (list[str]): List of input strings.

        Returns:
            Lava: The parsed Lava object.
        """

        max_x: int = 0
        max_y: int = 0
        max_z: int = 0
        points: list[Position] = []
        for line in input_lines:
            x, y, z = [int(element) for element in line.split(",")]
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)
            points.append(Position(x, y, z))

        return Lava(
            dimension_x=max_x + 1,
            dimension_y=max_y + 1,
            dimension_z=max_z + 1,
            points=points,
        )


def part_one(input_lines: list[str]) -> int:

    # Parse the input
    lava = Lava.from_text(input_lines)

    # Calculate the contact surface
    return lava.contact_surface()


def part_two(input_lines: list[str]) -> int:

    # Parse the input
    lava = Lava.from_text(input_lines)

    # Calculate the contact surface, without pockets of air
    return lava.contact_surface(without_pockets=True)


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_18.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
