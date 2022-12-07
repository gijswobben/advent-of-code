# https://adventofcode.com/2021/day/11

from __future__ import annotations

import itertools
from pathlib import Path

import numpy as np


class Octopus:
    def __init__(self, x: int, y: int, energy_level: int, grid: OctopusGrid) -> None:
        self.energy_level = energy_level
        self.n_flashes = 0
        self.x = x
        self.y = y
        self.grid = grid
        self.flashed = False

    def flash(self) -> None:
        if self.flashed:
            return None
        else:
            self.flashed = True
            self.n_flashes += 1

            for neighbour in self.all_neighbours:
                neighbour.energy_level += 1
                if neighbour.energy_level > 9:
                    neighbour.flash()

            return None

    def get_neighbour(self, x: int, y: int) -> Octopus | None:
        min_grid_x = 0
        max_grid_x = len(self.grid.state[0]) - 1
        min_grid_y = 0
        max_grid_y = len(self.grid.state) - 1

        if x < min_grid_x or x > max_grid_x or y < min_grid_y or y > max_grid_y:
            return None
        return self.grid.state[y][x]

    @property
    def left(self) -> Octopus | None:
        return self.get_neighbour(self.x - 1, self.y)

    @property
    def right(self) -> Octopus | None:
        return self.get_neighbour(self.x + 1, self.y)

    @property
    def top(self) -> Octopus | None:
        return self.get_neighbour(self.x, self.y - 1)

    @property
    def bottom(self) -> Octopus | None:
        return self.get_neighbour(self.x, self.y + 1)

    @property
    def top_left(self) -> Octopus | None:
        return self.get_neighbour(self.x - 1, self.y - 1)

    @property
    def top_right(self) -> Octopus | None:
        return self.get_neighbour(self.x + 1, self.y - 1)

    @property
    def bottom_left(self) -> Octopus | None:
        return self.get_neighbour(self.x - 1, self.y + 1)

    @property
    def bottom_right(self) -> Octopus | None:
        return self.get_neighbour(self.x + 1, self.y + 1)

    @property
    def all_neighbours(self) -> list[Octopus]:
        all_neighbours = [
            self.left,
            self.right,
            self.top,
            self.bottom,
            self.top_left,
            self.top_right,
            self.bottom_left,
            self.bottom_right,
        ]
        return [element for element in all_neighbours if element is not None]

    def __repr__(self) -> str:
        return f"{self.energy_level}"


class OctopusGrid:
    def __init__(self, initial_state: list[list[int]]) -> None:
        self.state: list[list[Octopus]] = []
        for y, row in enumerate(initial_state):
            new_row: list[Octopus] = []
            for x, value in enumerate(row):
                new_row.append(Octopus(x=x, y=y, energy_level=value, grid=self))
            self.state.append(new_row)

    def simulate(self, n_steps: int) -> OctopusGrid:
        for _ in range(n_steps):
            self.step()
        return self

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        output: list[str] = []
        for row in self.state:
            output.append(" ".join([str(octopus.energy_level) for octopus in row]))
        return "\n".join(output)

    def step(self):
        for octopus in itertools.chain.from_iterable(self.state):
            octopus.energy_level += 1

        n_flashes = len(
            [
                octopus
                for octopus in itertools.chain.from_iterable(self.state)
                if octopus.flashed
            ]
        )
        n_flashes_changed = True
        while n_flashes_changed:
            for octopus in itertools.chain.from_iterable(self.state):
                if octopus.energy_level > 9:
                    octopus.flash()
            n_flashes_new = len(
                [
                    octopus
                    for octopus in itertools.chain.from_iterable(self.state)
                    if octopus.flashed
                ]
            )
            n_flashes_changed = n_flashes != n_flashes_new
            n_flashes = n_flashes_new

        for octopus in itertools.chain.from_iterable(self.state):
            if octopus.energy_level > 9:
                octopus.energy_level = 0
                octopus.flashed = False

    @property
    def n_flashes(self) -> int:
        return int(
            np.sum(
                [
                    octopus.n_flashes
                    for octopus in itertools.chain.from_iterable(self.state)
                ]
            )
        )


def part_one(input_lines: list[str]) -> int:
    grid = OctopusGrid([[int(element) for element in row] for row in input_lines])
    grid.simulate(100)
    return grid.n_flashes


def part_two(input_lines: list[str]) -> int:
    grid = OctopusGrid([[int(element) for element in row] for row in input_lines])
    found = False
    n_simulations = 0
    while not found:
        grid.simulate(1)
        n_simulations += 1
        found = all(
            [
                octopus.energy_level == 0
                for octopus in itertools.chain.from_iterable(grid.state)
            ]
        )
    return n_simulations


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[2] / "data/year_2021/day_11.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
