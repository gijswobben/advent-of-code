"""Assignment for day 10 of 2024 Advent of Code.

https://adventofcode.com/2024/day/10
"""

from __future__ import annotations

from collections import namedtuple
from pathlib import Path

import networkx as nx
import numpy as np

Position = namedtuple("Position", ["x", "y", "height"])


class TopographicMap:
    """A class to represent a topographic map.

    Args:
    ----
        input_lines: The input lines (strings).

    """

    def __init__(self, input_lines: list[str]) -> None:
        # The input lines
        self.input_lines = input_lines

        # Map of the topographic heights
        self.heights = np.array([[int(char) for char in line] for line in input_lines])

        # For each point, check the surrounding points (up, down, left,
        # right) and add an edge to the graph if the next point is
        # exactly 1 higher than the current point.
        self.graph = nx.DiGraph()
        for y, row in enumerate(self.heights):
            for x, current_height in enumerate(row):
                current_position = Position(x=x, y=y, height=int(current_height))

                # Check the surrounding points
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_position = Position(
                        x=x + dx,
                        y=y + dy,
                        height=int(current_height + 1),
                    )
                    # Check if the new position is within the bounds of
                    # the map and if the height is exactly 1 higher than
                    # the current height.
                    if (
                        new_position.x >= 0
                        and new_position.x < self.heights.shape[1]
                        and new_position.y >= 0
                        and new_position.y < self.heights.shape[0]
                    ) and (
                        int(self.heights[new_position.y, new_position.x])
                        == current_height + 1
                    ):
                        self.graph.add_edge(current_position, new_position)

    def find_trailhead_score(self) -> int:
        """Add the scores for all the trailheads in the topographic map.

        Returns
        -------
            The scores for all the trailheads in the topographic map.

        """
        starting_points = [node for node in self.graph.nodes if node.height == 0]
        finish_points = [node for node in self.graph.nodes if node.height == 9]

        return sum(
            [
                sum(
                    1
                    for finish in finish_points
                    if nx.has_path(self.graph, start, finish)
                )
                for start in starting_points
            ],
        )

    def find_trailhead_rating(self) -> int:
        """Find the rating for the trailheads in the topographic map.

        Returns
        -------
            The rating for the trailheads in the topographic map.

        """
        starting_points = [node for node in self.graph.nodes if node.height == 0]
        finish_points = [node for node in self.graph.nodes if node.height == 9]

        return sum(
            [
                sum(
                    len(list(nx.all_simple_paths(self.graph, start, finish)))
                    for finish in finish_points
                    if nx.has_path(self.graph, start, finish)
                )
                for start in starting_points
            ],
        )


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    topographic_map = TopographicMap(input_lines)
    trailhead_score = topographic_map.find_trailhead_score()
    return trailhead_score


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    topographic_map = TopographicMap(input_lines)
    trailhead_rating = topographic_map.find_trailhead_rating()
    return trailhead_rating


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_10.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
