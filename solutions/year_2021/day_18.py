# https://adventofcode.com/2021/day/18

from __future__ import annotations

import functools
import math
from pathlib import Path


class SnailNumber:
    def __init__(
        self,
        value: list,
        depth: int = 0,
        parent: SnailNumber | None = None,
    ) -> None:

        # Store inputs
        self._depth = depth
        self._parent = parent

        # Parse nested SnailNumbers
        self._value: list[SnailNumber | int] = []
        for v in value:
            if isinstance(v, int):
                self._value.append(v)
            elif isinstance(v, list):
                self._value.append(SnailNumber(v, depth=depth + 1, parent=self))
            else:
                self._value.append(v)

    def __add__(self, other: SnailNumber) -> SnailNumber:
        return SnailNumber(value=[self._value, other._value])

    def reduce(
        self, depth: int = 0, parent: SnailNumber | None = None, parent_index: int = 0
    ) -> SnailNumber:
        # Explode
        if depth >= 4:
            print(f"Explode {self} ({parent})")

        # Split
        else:
            ...

        # def _split(level: list[SnailNumber | int]) -> list[SnailNumber | int]:
        #     for index, value in enumerate(level):
        #         if isinstance(value, int) and value >= 10:
        #             level[index] = SnailNumber(
        #                 [
        #                     math.floor(value / 2),
        #                     math.ceil(value / 2),
        #                 ]
        #             )
        #         elif isinstance(value, SnailNumber):
        #             level[index] = SnailNumber(_split(value._value))
        #     return level

        for index, value in enumerate(self._value[:]):
            if isinstance(value, SnailNumber):
                value.reduce(depth=depth + 1, parent=self, parent_index=index)

        return self

    @property
    def magnitude(self) -> int:
        return sum(
            element * multiplier
            if isinstance(element, int)
            else element.magnitude * multiplier
            for element, multiplier in zip(
                self._value, range(3, 3 - min(len(self._value), 3), -1)
            )
        )

    def __repr__(self) -> str:
        return f"SnailNumber({self._value})"


def part_one(input_lines: list[str]) -> int:

    numbers: list[SnailNumber] = [eval(line, {}, {}) for line in input_lines]

    print(SnailNumber([[[[[9, 8], 1], 2], 3], 4]).reduce())
    # print(SnailNumber([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]).reduce())

    return functools.reduce(lambda a, b: a + b, numbers).magnitude


def part_two(input_lines: list[str]) -> int:
    return 0


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_18.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
