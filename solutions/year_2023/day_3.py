"""Assignment for day 3 of 2023 Advent of Code.

https://adventofcode.com/2023/day/3
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Position:

    """Helper class to keep track of positions in the engine."""

    row: int
    column: int


class Part:

    """Individual part of the engine."""

    def __init__(self, positions: list[Position], value: int, engine: Engine) -> None:
        """Create a new part.

        Args:
        ----
            positions (list[Position]): The positions covered by the
                part.
            value (int): The value of the part (part number).
            engine (Engine): Reference to the engine.
        """
        self.positions = positions
        self.value = value
        self.engine = engine

    @property
    def is_part_number(self) -> bool:
        """A part is a part number if it is connected to any symbol.

        Returns
        -------
            bool: Whether the part is a part number.
        """
        # Determine the adjecent positions
        adjecent_positions = get_adjecent_positions(self.positions)

        # Get the values for the adjecent positions
        adjecent_values = []
        for position in adjecent_positions:
            # Skip out of bound positions
            if (
                position.column < 0
                or position.row < 0
                or position.column >= len(self.engine.definition)
                or position.row >= len(self.engine.definition[0])
            ):
                continue
            adjecent_values.append(
                self.engine.definition[position.row][position.column],
            )

        return not all(value == "." for value in adjecent_values)


class Gear:

    """Gear in the engine."""

    def __init__(self, positions: list[Position], engine: Engine) -> None:
        """Create a new gear.

        Args:
        ----
            positions (list[Position]): The positions covered by the
                gear.
            engine (Engine): The engine.
        """
        self.positions = positions
        self.engine = engine

    @property
    def connected_parts(self) -> list[Part]:
        """List of parts that are connected to the gear.

        Returns
        -------
            list[Part]: List of parts.
        """
        # Get all the adjecent positions
        adjecent_position = get_adjecent_positions(self.positions)

        # Get all the parts that are connected to the gear by checking
        # the adjecent positions
        connected_parts = []
        for part in self.engine.parts:
            for position in adjecent_position:
                if position in part.positions:
                    connected_parts.append(part)
                    break

        return connected_parts

    @property
    def ratio(self) -> int | None:
        """Gear ratio for this gear.

        Gears only have a ratio when there are exactly two parts
        connected.

        Returns
        -------
            int | None: The ratio or None.
        """
        if not self.is_connected:
            return None
        return self.connected_parts[0].value * self.connected_parts[1].value

    @property
    def is_connected(self) -> bool:
        """Whether or not this gear is connected to exactly two parts.

        Returns
        -------
            bool: Whether or not this gear is connected to exactly two
                parts.
        """
        return len(self.connected_parts) == 2


class Engine:

    """Engine of the machine."""

    def __init__(self, definition: list[str]) -> None:
        """Create a new engine.

        Args:
        ----
            definition (list[str]): The definition of the engine.
        """
        self.parts: list[Part] = []
        self.gears: list[Gear] = []
        self.definition = definition

        # Extract all the parts
        for row, line in enumerate(definition):
            matches = re.finditer(r"\d+", line)

            for m in matches:
                self.parts.append(
                    Part(
                        positions=[
                            Position(row, column) for column in range(*m.span())
                        ],
                        value=int(m.group()),
                        engine=self,
                    ),
                )

        # Extract all the gears
        for row, line in enumerate(definition):
            matches = re.finditer(r"\*", line)

            for m in matches:
                self.gears.append(
                    Gear(
                        positions=[
                            Position(row, column) for column in range(*m.span())
                        ],
                        engine=self,
                    ),
                )


def get_adjecent_positions(positions: list[Position]) -> list[Position]:
    """Make a list of all the adjecent positions.

    Args:
    ----
        positions (list[Position]): The positions to get the adjecent
            positions for.

    Returns:
    -------
        list[Position]: The adjecent positions.
    """
    adjecent_positions = [
        Position(positions[0].row + 1, positions[0].column - 1),  # bottom-left corner
        Position(positions[0].row, positions[0].column - 1),  # left
        Position(positions[0].row - 1, positions[0].column - 1),  # top-left corner
        *[
            Position(position.row - 1, position.column) for position in positions
        ],  # up for every position
        Position(positions[0].row + 1, positions[-1].column + 1),  # bottom-right corner
        Position(positions[0].row, positions[-1].column + 1),  # right
        Position(positions[0].row - 1, positions[-1].column + 1),  # top-right corner
        *[
            Position(position.row + 1, position.column) for position in positions
        ],  # down for every position
    ]
    return adjecent_positions


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.
    """
    # Create an engine from the input
    engine = Engine(input_lines)

    # Get all the parts that are part numbers
    engine_parts = [part for part in engine.parts if part.is_part_number]

    # Return the sum of the values of the parts
    return sum(part.value for part in engine_parts)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.
    """
    # Create an engine from the input
    engine = Engine(input_lines)

    # Get all the gears that are connected to parts
    gears = [gear for gear in engine.gears if gear.is_connected]

    # Return the sum of the ratios of the gears
    return sum(gear.ratio for gear in gears if gear.ratio is not None)


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_3.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
