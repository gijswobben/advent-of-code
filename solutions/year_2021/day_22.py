# https://adventofcode.com/2021/day/22

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

INPUT_PATTERN = re.compile(
    r"(?P<state>\w+)\sx=(?P<min_x>-?\d+)\.\.(?P<max_x>-?\d+),y=(?P<min_y>-?\d+)\.\.(?P<max_y>-?\d+),z=(?P<min_z>-?\d+)\.\.(?P<max_z>-?\d+)"
)


class State(IntEnum):
    OFF = 0
    ON = 1


@dataclass(frozen=True)
class Cuboid:
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    @property
    def n_cubes_on(self) -> int:
        return (
            (self.max_x - self.min_x)
            * (self.max_y - self.min_y)
            * (self.max_z - self.min_z)
        )

    def overlaps_with(self, other: Cuboid) -> bool:
        return (
            (
                (self.min_x <= other.min_x and other.min_x <= self.max_x)
                or (other.min_x <= self.min_x and self.min_x <= other.max_x)
            )
            and (
                (self.min_y <= other.min_y and other.min_y <= self.max_y)
                or (other.min_y <= self.min_y and self.min_y <= other.max_y)
            )
            and (
                (self.min_z <= other.min_z and other.min_z <= self.max_z)
                or (other.min_z <= self.min_z and self.min_z <= other.max_z)
            )
        )

    def split(self) -> set[Cuboid]:
        ...


class ReactorCore:
    def __init__(self) -> None:
        self._cuboids: set[Cuboid] = set()

    @property
    def n_cubes_on(self) -> int:
        return sum(cuboid.n_cubes_on for cuboid in self._cuboids)

    def switch(self, state: State, cuboid: Cuboid) -> None:

        # Determine overlapping cuboids
        overlapping: list[Cuboid] = [
            c for c in self._cuboids if c.overlaps_with(cuboid)
        ]

        if state == State.ON:

            # No overlap, just add the cuboid to the list
            if len(overlapping) == 0:
                print("add", cuboid)
                self._cuboids.add(cuboid)

            # Overlap, split the cuboid in unique, non-overlapping
            # cuboids
            else:

                cuboid.split()

        else:

            # No overlap, skip
            if len(overlapping) == 0:
                return

            else:
                ...

    # def switch(
    #     self,
    #     state: State,
    #     min_x: int,
    #     max_x: int,
    #     min_y: int,
    #     max_y: int,
    #     min_z: int,
    #     max_z: int,
    #     limit_min: int | None = None,
    #     limit_max: int | None = None,
    # ) -> None:

    #     if limit_min is not None and limit_max is not None:
    #         if (
    #             max_x <= limit_min
    #             or max_y <= limit_min
    #             or max_z <= limit_min
    #             or min_x >= limit_max
    #             or min_y >= limit_max
    #             or min_z >= limit_max
    #         ):
    #             return

    #     if state == State.ON:
    #         taken_positions: set[Position] = set(
    #             [cube.position for cube in self._cubes]
    #         )
    #         for x in range(min_x, max_x + 1):
    #             for y in range(min_y, max_y + 1):
    #                 for z in range(min_z, max_z + 1):
    #                     position = Position(x, y, z)
    #                     if position not in taken_positions:
    #                         self._cubes.append(Cube(state=state, position=position))

    #     else:
    #         self._cubes = [
    #             cube
    #             for cube in self._cubes
    #             if not cube.is_in_cuboid(min_x, max_x, min_y, max_y, min_z, max_z)
    #         ]


def part_one(input_lines: list[str]) -> int:
    reactor = ReactorCore()
    for line in input_lines:
        match = re.search(INPUT_PATTERN, line)
        if match is None:
            raise Exception("Invalid input")
        state = State[match.group("state").upper()]
        min_x = int(match.group("min_x"))
        max_x = int(match.group("max_x"))
        min_y = int(match.group("min_y"))
        max_y = int(match.group("max_y"))
        min_z = int(match.group("min_z"))
        max_z = int(match.group("max_z"))
        reactor.switch(state, Cuboid(min_x, max_x, min_y, max_y, min_z, max_z))

    return reactor.n_cubes_on


def part_two(input_lines: list[str]) -> int:
    return 0


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_22.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
