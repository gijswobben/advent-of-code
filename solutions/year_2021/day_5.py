# https://adventofcode.com/2021/day/5
from __future__ import annotations

import itertools
from pathlib import Path

import numpy as np
import pandas as pd


class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def __repr__(self) -> str:
        return f"Line<({self.x1},{self.y1}), ({self.x2},{self.y2})>"

    def _positions(self) -> list[tuple[int, int]]:
        x_left = self.x1 if self.x1 <= self.x2 else self.x2
        x_right = self.x1 if self.x1 > self.x2 else self.x2

        y_top = self.y1 if self.y1 <= self.y2 else self.y2
        y_bottom = self.y1 if self.y1 > self.y2 else self.y2

        x_steps = list(range(x_left, x_right + 1))
        y_steps = list(range(y_top, y_bottom + 1))

        if self.x2 > self.x1:
            x_steps.reverse()

        if self.y2 > self.y1:
            y_steps.reverse()

        return list(
            zip(x_steps, itertools.cycle(y_steps))
            if len(x_steps) > len(y_steps)
            else zip(itertools.cycle(x_steps), y_steps)
        )

    def draw(self, grid: pd.DataFrame) -> pd.DataFrame:

        for x, y in self._positions():
            grid.iloc[y, x] += 1
        return grid

    @classmethod
    def from_text(cls, text: str) -> Line:
        source, target = text.split(" -> ")
        source_x, source_y = [int(element) for element in source.split(",")]
        target_x, target_y = [int(element) for element in target.split(",")]
        return Line(x1=source_x, y1=source_y, x2=target_x, y2=target_y)


def count_intersections(grid: pd.DataFrame) -> int:
    return grid.where(grid >= 2).count(axis=1).sum()


def part_one(input_lines: list[str]) -> int:

    lines = [Line.from_text(line.strip()) for line in input_lines]

    # Find the ranges
    max_x = max([line.x1 for line in lines] + [line.x2 for line in lines]) + 1
    max_y = max([line.y1 for line in lines] + [line.y2 for line in lines]) + 1

    # Create a grid that can hold all the lines
    grid = pd.DataFrame(np.zeros((max_y, max_x)))

    # Only consider horizontal and vertical lines
    for line in lines:
        if (line.x1 == line.x2) or (line.y1 == line.y2):
            grid = line.draw(grid)
    return count_intersections(grid)


def part_two(input_lines: list[str]) -> int:

    lines = [Line.from_text(line.strip()) for line in input_lines]

    # Find the ranges
    max_x = max([line.x1 for line in lines] + [line.x2 for line in lines]) + 1
    max_y = max([line.y1 for line in lines] + [line.y2 for line in lines]) + 1

    # Create a grid that can hold all the lines
    grid = pd.DataFrame(np.zeros((max_y, max_x)))

    # Only consider horizontal and vertical lines
    for line in lines:
        grid = line.draw(grid)

    return count_intersections(grid)


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_5.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
