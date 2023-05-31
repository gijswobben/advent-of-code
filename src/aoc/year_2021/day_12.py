# https://adventofcode.com/2021/day/12

from __future__ import annotations

import itertools
from copy import copy
from pathlib import Path


class Cave:
    def __init__(self, name: str) -> None:
        self.name = name
        self.links: list[Cave] = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.name}>"


class SmallCave(Cave):
    ...


class LargeCave(Cave):
    ...


class Submarine:
    def __init__(self, cave_system: CaveSystem) -> None:
        self.cave_system = cave_system

    def find_paths(self) -> list[list[Cave]]:
        def _traverse_path(path: list[Cave], visited_map: dict[Cave, bool]):
            paths: list[list[Cave]] = [
                [path[-1], link]
                for link in path[-1].links
                if not visited_map.get(link, False)
            ]

            for sub_path in paths:

                if (
                    len([link for link in path[-1].links if link not in visited_map])
                    == 0
                ):
                    return []

                # Path ended in the finish
                if path[-1] == self.cave_system.end:
                    continue

                path.extend(
                    _traverse_path(
                        sub_path,
                        visited_map={
                            cave: cave in path
                            for cave in self.cave_system.caves
                            if isinstance(cave, SmallCave)
                        },
                    )
                )

            return paths

        visited_map: dict[Cave, bool] = {
            cave: False
            for cave in self.cave_system.caves
            if isinstance(cave, SmallCave)
        }
        paths = _traverse_path(path=[self.cave_system.start], visited_map=visited_map)

        return paths


class CaveSystem:
    def __init__(self, caves: list[Cave]) -> None:
        self.caves = caves
        self.start = next(
            (cave for cave in caves if cave.name == "start"), SmallCave("start")
        )
        self.end = next(
            (cave for cave in caves if cave.name == "end"), SmallCave("end")
        )

    @classmethod
    def from_text(cls, input_lines: list[str]) -> CaveSystem:

        # First pass to create the caves
        caves: dict[str, Cave] = {"start": SmallCave("start"), "end": SmallCave("end")}
        cave_names = set(
            itertools.chain.from_iterable(
                [
                    [
                        cave
                        for cave in line.split("-")
                        if cave != "start" and cave != "end"
                    ]
                    for line in input_lines
                ]
            )
        )
        for cave in cave_names:
            caves[cave] = LargeCave(cave) if cave.isupper() else SmallCave(cave)

        # Second pass to create all the relations
        for line in input_lines:
            source, target = line.split("-")
            caves[source].links.append(caves[target])
            caves[target].links.append(caves[source])

        return CaveSystem(caves=list(caves.values()))


def part_one(input_lines: list[str]) -> int:

    # Create the cave system from the input
    cave_system = CaveSystem.from_text(input_lines=input_lines)

    # Create the submarine and give it the map to the cave system
    submarine = Submarine(cave_system=cave_system)

    # Use the submarine to fine all paths
    paths = submarine.find_paths()
    print(paths)

    # Count the number of paths possible
    return len(paths)


def part_two(input_lines: list[str]) -> int:
    return 0


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_12.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
