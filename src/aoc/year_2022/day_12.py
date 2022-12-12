# https://adventofcode.com/2022/day/12

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from string import ascii_lowercase

import networkx as nx
import numpy as np


class Direction(Enum):
    """Class that represents the direction in which the head can move."""

    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


@dataclass
class Coordinate:
    """Class that represents a set of coordinates."""

    x: int
    y: int


class HeightMap:
    """Represents the map with different heights.

    Args:
        heights (list[list[int]]): The height at all locations in the
            map.
        start (Coordinate): The start position on the map.
        finish (Coordinate): The finish position on the map.
    """

    def __init__(
        self, heights: list[list[int]], start: Coordinate, finish: Coordinate
    ) -> None:
        self._start = start
        self._finish = finish
        self._map = np.array(heights)
        self._graph = self.create_graph()

    def get_low_points(self) -> list[Coordinate]:
        """Make a list of all the lowest points on the map.

        Returns:
            list[Coordinate]: List of coordinates where the height is
                the lowest.
        """

        # Get the lowest point on the map
        low_point_height = np.min(self._map)

        # Create a list of lowest points on the map
        low_points: list[Coordinate] = []
        for y in range(self._map.shape[0]):
            for x in range(self._map.shape[1]):
                if self._map[y, x] == low_point_height:
                    low_points.append(Coordinate(x, y))
        return low_points

    def __repr__(self) -> str:
        output: list[str] = []
        output.append(f"HeightMap<start: {self._start}, finish: {self._finish}>")
        output.append("=" * 40)
        output.append(str(self._map))
        return "\n".join(output)

    def create_graph(self) -> nx.DiGraph:
        """Create a directed graph that contains nodes for each location
        on the map, and a link between the nodes if it is possible to
        move between 2 locations.

        Returns:
            nx.DiGraph: The directed graph.
        """
        graph = nx.DiGraph()
        for y in range(self._map.shape[0]):
            for x in range(self._map.shape[1]):
                available_paths = [
                    ((x, y), (move.x, move.y))
                    for move in self.get_available_moves(position=Coordinate(x=x, y=y))
                ]
                graph.add_edges_from(available_paths)
        return graph

    def find_shortest_path(
        self, start: Coordinate | None = None, finish: Coordinate | None = None
    ) -> list[Coordinate]:
        """Find the shortest path from start to finish.

        Args:
            start (Coordinate | None, optional): The start point, set to
                the map startpoint if not provided. Defaults to None.
            finish (Coordinate | None, optional): The finish point, set
                to the map finishpoint if not provided. Defaults to
                None.

        Returns:
            _type_: _description_
        """
        if start is None:
            start = self._start
        if finish is None:
            finish = self._finish

        path = nx.shortest_path(
            self._graph,
            source=(start.x, start.y),
            target=(finish.x, finish.y),
        )
        return [Coordinate(*element) for element in path]

    def get_available_moves(self, position: Coordinate) -> list[Coordinate]:
        """Get a list of all available moves from a particular staring
        position.

        Args:
            position (Coordinate): The starting position.

        Returns:
            list[Coordinate]: List of coordinates that can be reached
                from this position.
        """

        # Get the height at the requested position
        height_at_position = self._map[position.y, position.x]

        # Loop all possible directions we can move in
        output: list[Coordinate] = []
        for direction in Direction:

            # Get the coordinates of the position after moving in a
            # particular direction
            next_position = Coordinate(
                x=position.x + direction.value[0],
                y=position.y + direction.value[1],
            )

            # Check if a move is valid
            if (
                # Stay on the map
                next_position.x >= 0
                and next_position.x < self._map.shape[1]
                and next_position.y >= 0
                and next_position.y < self._map.shape[0]
                # Destination square can be at most one higher than the
                # elevation of your current square
                and self._map[next_position.y, next_position.x] - height_at_position
                <= 1
            ):
                output.append(next_position)

        # Return all valid moves
        return output

    @classmethod
    def from_text(cls, input_lines: list[str]) -> HeightMap:
        """Create a new HeightMap from a list of strings.

        Args:
            input_lines (list[str]): The list of text that define the
                map.

        Returns:
            HeightMap: The resulting height map.
        """

        # Initialize the variables
        heights: list[list[int]] = []
        start: Coordinate = Coordinate(0, 0)
        finish: Coordinate = Coordinate(0, 0)

        # Loop the input lines
        for y, line in enumerate(input_lines):
            map_line: list[int] = []

            # Loop the characters in the line
            for x, character in enumerate(line):

                # Store the starting position
                if character == "S":
                    character = "a"
                    start = Coordinate(x, y)

                # Store the finish position
                elif character == "E":
                    character = "z"
                    finish = Coordinate(x, y)

                # Convert the character into a height
                map_line.append(ascii_lowercase.index(character) + 1)
            heights.append(map_line)

        # Create the height map
        return HeightMap(heights=heights, start=start, finish=finish)


def part_one(input_lines: list[str]) -> int:

    # Create a new height map
    heights_map = HeightMap.from_text(input_lines=input_lines)

    # Get the shortest path from start to finish
    shortest_path = heights_map.find_shortest_path()
    shortest_path_length = len(shortest_path) - 1  # exclude the start
    return shortest_path_length


def part_two(input_lines: list[str]) -> int:

    # Create a new height map
    heights_map = HeightMap.from_text(input_lines=input_lines)

    # Get all lowest points on the map
    starting_points = heights_map.get_low_points()

    # Get the shortest path from all starting points to the finish
    shortest_path_lengths: list[int] = []
    for start in starting_points:
        try:
            shortest_path_lengths.append(
                len(heights_map.find_shortest_path(start=start)) - 1
            )
        except:
            pass

    # Get the length shortest path
    shortest_path_length = np.min(shortest_path_lengths)
    return shortest_path_length


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_12.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
