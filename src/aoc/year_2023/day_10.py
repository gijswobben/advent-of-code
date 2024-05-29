"""Assignment for day 10 of 2023 Advent of Code.

https://adventofcode.com/2023/day/10
"""

from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from rich import print

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.

DIRECTION_MAP = {
    "|": [
        (-1, 0),  # North
        (1, 0),  # South
    ],
    "-": [
        (0, -1),  # West
        (0, 1),  # East
    ],
    "L": [
        (-1, 0),  # North
        (0, 1),  # East
    ],
    "J": [
        (-1, 0),  # North
        (0, -1),  # West
    ],
    "7": [
        (1, 0),  # South
        (0, -1),  # West
    ],
    "F": [
        (1, 0),  # South
        (0, 1),  # East
    ],
}


class Maze:
    def __init__(self, input_lines: list[str]) -> None:
        self.graph = nx.Graph()

        # Add the nodes
        for row, line in enumerate(input_lines):
            for column, char in enumerate(line):
                if char == "S":
                    self.start = (row, column)
                if char != ".":
                    self.graph.add_node((row, column))

        # Add the edges
        for row, line in enumerate(input_lines):
            for column, char in enumerate(line):
                if char in DIRECTION_MAP:
                    for direction in DIRECTION_MAP[char]:
                        new_row = row + direction[0]
                        new_column = column + direction[1]
                        self.graph.add_edge((row, column), (new_row, new_column))

        # Remove all nodes that are not connected to the start
        remove_nodes = []
        for node in self.graph.nodes:
            if not nx.has_path(self.graph, self.start, node):
                remove_nodes.append(node)
        self.graph.remove_nodes_from(remove_nodes)

    def find_main_cycle(self):
        return nx.find_cycle(self.graph, self.start)

    def filter(self, cycle: list[tuple[int, int]]):
        final_edges = [
            (source, target)
            for (source, target) in self.graph.edges
            if (source, target) not in cycle and (target, source) not in cycle
        ]
        self.graph.remove_edges_from(final_edges)

        # Remove the nodes that are not connected to the start
        remove_nodes = []
        for node in self.graph.nodes:
            if not nx.has_path(self.graph, self.start, node):
                remove_nodes.append(node)

        self.graph.remove_nodes_from(remove_nodes)


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.
    """
    maze = Maze(input_lines)
    cycle = maze.find_main_cycle()

    maze.filter(cycle)

    layers = list(nx.bfs_layers(maze.graph, sources=[maze.start]))
    print(("layers", layers))
    nx.draw(maze.graph, with_labels=True)
    plt.show()
    return len(layers) - 1


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.
    """
    return 0


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_10.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
