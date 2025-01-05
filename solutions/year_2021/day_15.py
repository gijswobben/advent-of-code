# https://adventofcode.com/2021/day/15

from __future__ import annotations

from enum import Enum
from pathlib import Path

import networkx as nx
import numpy as np


class Neighbours(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    TOP = (0, -1)
    BOTTOM = (0, 1)

    def to_absolute(self, position: tuple[int, int]) -> tuple[int, int]:
        return (position[0] + self.value[0], position[1] + self.value[1])


class Cave:
    """Represents the cave.

    Args:
        grid (np.ndarray): The risk values for all the positions in the
            cave.
    """

    def __init__(self, grid: np.ndarray) -> None:
        self.grid = grid

        # Create a weighted graph between all positions in the grid
        self.graph = nx.DiGraph()
        for (y, x), _ in np.ndenumerate(grid):

            # List all valid neighbours and make edges to those
            # neighbours
            neighbours = [
                neighbour
                for neighbour in [
                    neighbour.to_absolute((x, y)) for neighbour in Neighbours
                ]
                if 0 <= neighbour[0] < self.grid.shape[1]
                and 0 <= neighbour[1] < self.grid.shape[0]
            ]

            # Weight is the value of the neighbour, cost of entering
            for neighbour in neighbours:
                self.graph.add_edge(
                    (x, y), neighbour, weight=self.grid[neighbour[1], neighbour[0]]
                )

    def find_low_risk_path(self) -> int:
        """Find the path with the lowest risk score.

        Returns:
            int: The risk score of the shortest path with the lowest
                score.
        """

        start = (0, 0)  # Top left
        end = (self.grid.shape[1] - 1, self.grid.shape[0] - 1)  # Bottom right

        # Calculate the shortest path with weights
        path = nx.dijkstra_path(self.graph, start, end)

        # Get all the corresponding values, skip the first element
        return int(sum([self.grid[position[1], position[0]] for position in path[1:]]))

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Cave:
        """Create a cave from a text representation.

        Args:
            input_lines (list[str]): The input lines as a string of list
                values per row.

        Returns:
            Cave: The parsed Cave object.
        """
        grid = np.zeros((len(input_lines), len(input_lines[0])))
        for y, line in enumerate(input_lines):
            for x, value in enumerate(line):
                grid[y, x] = int(value)
        return Cave(grid=grid)

    @classmethod
    def from_tiles(cls, input_lines: list[str]) -> Cave:
        """Create a cave from a text representation.

        Treat the input as a tile in a 5x5 matrix. Next tiles have
        higher risk scores.

        Args:
            input_lines (list[str]): The input lines as a string of list
                values per row.

        Returns:
            Cave: The parsed Cave object.
        """

        # Parse the input as a single tile
        tile = np.zeros((len(input_lines), len(input_lines[0])))
        for y, line in enumerate(input_lines):
            for x, value in enumerate(line):
                tile[y, x] = int(value)

        # Repeat the tile in all directions with small modifications
        for axis in [0, 1]:
            tiles: list[np.ndarray] = [tile]
            for _ in range(1, 5):

                # Next tile is a copy of the last
                t = tiles[-1].copy()

                # Wrap values that will go over 9
                t[t == 9] = 0
                t = t + 1
                tiles.append(t)
            tile = np.concatenate(tiles, axis=axis)

        return Cave(grid=tile)


def part_one(input_lines: list[str]) -> int:
    cave = Cave.from_text(input_lines)
    return cave.find_low_risk_path()


def part_two(input_lines: list[str]) -> int:
    cave = Cave.from_tiles(input_lines)
    return cave.find_low_risk_path()


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_15.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
