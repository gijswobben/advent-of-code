"""Assignment for day 8 of 2023 Advent of Code.

https://adventofcode.com/2023/day/8
"""

from __future__ import annotations
import collections

import itertools
from pathlib import Path
from enum import StrEnum
from typing import Any, Generator
import more_itertools
from rich import print

import re

node_pattern = re.compile(r"(?P<node>\w{3}) = \((?P<left>\w{3}), (?P<right>\w{3})\)")


class Directions(StrEnum):
    LEFT = "L"
    RIGHT = "R"


def principal_period(s):
    i = (s + s).find(s, 1, -1)
    return None if i == -1 else s[:i]


def find_repeating_pattern(sequence: list[str]) -> list[str]:
    pp = None
    counter = 1
    while counter < len(sequence):
        # print(counter)
        # print("".join(sequence[:counter]))
        pp = principal_period("".join(sequence[:counter]))
        if pp is not None:
            return sequence[:counter]
        counter += 1
    return None


class Map:
    def __init__(self, trees: dict[str, tuple[str, str]]) -> None:
        self.trees = trees

    def walk(
        self,
        instructions: list[Directions],
        source: str = "AAA",
        destination: str = "ZZZ",
        max_steps: int = -1,
    ) -> list[str]:
        current_node = source
        path = []
        for instruction in itertools.cycle(instructions):
            if instruction == Directions.LEFT:
                current_node = self.trees[current_node][0]
            elif instruction == Directions.RIGHT:
                current_node = self.trees[current_node][1]

            path.append(current_node)

            if current_node == destination or len(path) == max_steps:
                return path

    def gost_walk(self, instructions: list[Directions]) -> int:
        # TODO: Walk in cycles; determine the length of the cycle; determine the number of cycles
        # before overlap

        # Find the start nodes and end nodes
        start_nodes = []
        end_nodes = []
        for node in self.trees.keys():
            if node.endswith("A"):
                start_nodes.append(node)
            elif node.endswith("Z"):
                end_nodes.append(node)

        path_samples = [
            self.walk(
                instructions=instructions.copy(),
                source=start_node,
                max_steps=1000 * len(instructions),
            )
            for start_node in start_nodes
        ]

        # Find the shortest sequence length
        sequence_lengths = [find_repeating_pattern(path) for path in path_samples]
        print(sequence_lengths)


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.
    """

    # Infinite repeat of the instructions at the top of the input
    instructions = [
        Directions.LEFT if instruction == "L" else Directions.RIGHT
        for instruction in input_lines[0]
    ]

    # Parse the tree
    trees: dict[str, tuple[str, str]] = {}
    for line in input_lines[2:]:
        match = node_pattern.match(line)
        if match:
            trees[match.group("node")] = (match.group("left"), match.group("right"))
    map = Map(trees)

    # Walk the map, count the steps
    path = map.walk(instructions=instructions)

    # Return the result
    return len(path)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.
    """

    # Infinite repeat of the instructions at the top of the input
    instructions = [
        Directions.LEFT if instruction == "L" else Directions.RIGHT
        for instruction in input_lines[0]
    ]

    # Parse the tree
    trees: dict[str, tuple[str, str]] = {}
    for line in input_lines[2:]:
        match = node_pattern.match(line)
        if match:
            trees[match.group("node")] = (match.group("left"), match.group("right"))
    map = Map(trees)

    # Walk the map, count the steps
    n_steps = map.gost_walk(instructions=instructions)

    # Return the result
    return n_steps


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_8.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
