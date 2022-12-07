# https://adventofcode.com/2021/day/9

from __future__ import annotations

import itertools
from pathlib import Path


class Cell:
    def __init__(self, x: int, y: int, value: int, grid: list[list[Cell]]) -> None:
        self.x = x
        self.y = y
        self.value = value
        self.grid = grid

    def __repr__(self) -> str:
        return f"{self.value}"

    def get_neighbour(self, x: int, y: int) -> Cell | None:
        min_grid_x = 0
        max_grid_x = len(self.grid[0]) - 1
        min_grid_y = 0
        max_grid_y = len(self.grid) - 1

        if x < min_grid_x or x > max_grid_x or y < min_grid_y or y > max_grid_y:
            return None
        return self.grid[y][x]

    @property
    def neighbour_left(self) -> Cell | None:
        return self.get_neighbour(self.x - 1, self.y)

    @property
    def neighbour_right(self) -> Cell | None:
        return self.get_neighbour(self.x + 1, self.y)

    @property
    def neighbour_top(self) -> Cell | None:
        return self.get_neighbour(self.x, self.y - 1)

    @property
    def neighbour_bottom(self) -> Cell | None:
        return self.get_neighbour(self.x, self.y + 1)

    @property
    def has_higher_neighbour(self) -> bool:
        return (
            (self.neighbour_left is not None and self.neighbour_left.value > self.value)
            or (
                self.neighbour_right is not None
                and self.neighbour_right.value > self.value
            )
            or (
                self.neighbour_top is not None and self.neighbour_top.value > self.value
            )
            or (
                self.neighbour_bottom is not None
                and self.neighbour_bottom.value > self.value
            )
        )

    @property
    def is_low_point(self) -> bool:
        return (
            (
                (
                    self.neighbour_left is not None
                    and self.neighbour_left.value > self.value
                )
                or self.neighbour_left is None
            )
            and (
                (
                    self.neighbour_right is not None
                    and self.neighbour_right.value > self.value
                )
                or self.neighbour_right is None
            )
            and (
                (
                    self.neighbour_top is not None
                    and self.neighbour_top.value > self.value
                )
                or self.neighbour_top is None
            )
            and (
                (
                    self.neighbour_bottom is not None
                    and self.neighbour_bottom.value > self.value
                )
                or self.neighbour_bottom is None
            )
        )


def calculate_risk_level(height_map: list[list[int]]) -> int:

    grid: list[list[Cell]] = []
    for y, row in enumerate(height_map):
        new_line: list[Cell] = []
        for x, value in enumerate(row):
            new_line.append(Cell(x, y, value, grid))
        grid.append(new_line)

    total = 0
    for cell in itertools.chain.from_iterable(grid):
        if cell.is_low_point:
            total += 1 + cell.value

    return total


def detect_basins(height_map: list[list[int]]) -> list[list[Cell]]:

    grid: list[list[Cell]] = []
    for y, row in enumerate(height_map):
        new_line: list[Cell] = []
        for x, value in enumerate(row):
            new_line.append(Cell(x, y, value, grid))
        grid.append(new_line)

    low_points: list[Cell] = []
    for cell in itertools.chain.from_iterable(grid):
        if cell.is_low_point:
            low_points.append(cell)

    basins: dict[Cell, list[Cell]] = {
        low_point: [low_point] for low_point in low_points
    }
    for low_point, basin in basins.items():
        size_changed = True
        while size_changed:
            basin_size = len(basin)
            for point in basin:
                if (
                    point.neighbour_left is not None
                    and point.neighbour_left.value > point.value
                    and point.neighbour_left not in basin
                    and point.neighbour_left.value != 9
                ):
                    basin.append(point.neighbour_left)
                if (
                    point.neighbour_right is not None
                    and point.neighbour_right.value > point.value
                    and point.neighbour_right not in basin
                    and point.neighbour_right.value != 9
                ):
                    basin.append(point.neighbour_right)
                if (
                    point.neighbour_top is not None
                    and point.neighbour_top.value > point.value
                    and point.neighbour_top not in basin
                    and point.neighbour_top.value != 9
                ):
                    basin.append(point.neighbour_top)
                if (
                    point.neighbour_bottom is not None
                    and point.neighbour_bottom.value > point.value
                    and point.neighbour_bottom not in basin
                    and point.neighbour_bottom.value != 9
                ):
                    basin.append(point.neighbour_bottom)
            size_changed = len(basin) == basin_size

    return list(basins.values())


def part_one(input_lines: list[str]) -> int:
    risk_level = calculate_risk_level(
        [[int(element) for element in row] for row in input_lines]
    )
    return risk_level


def part_two(input_lines: list[str]) -> int:
    basins = detect_basins([[int(element) for element in row] for row in input_lines])
    basin_sizes = sorted([len(basin) for basin in basins], reverse=True)
    total = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
    return total


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[2] / "data/year_2021/day_9.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
