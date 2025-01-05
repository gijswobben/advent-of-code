"""Assignment for day 8 of 2024 Advent of Code.

https://adventofcode.com/2024/day/8
"""

import itertools
from collections import defaultdict, namedtuple
from pathlib import Path

Antenna = namedtuple("Antenna", ["x", "y", "frequency"])
Antinode = namedtuple("Antinode", ["x", "y"])


class Map:
    def __init__(self, width: int, height: int, antennas: list[Antenna]) -> None:
        self.width = width
        self.height = height
        self.antennas = antennas

    def find_antinodes(self, with_harmonics: bool = False) -> list[Antinode]:
        antinodes: list[Antinode] = []

        # Antinodes can only occur for same frequency antennas
        antennas: dict[str, list[Antenna]] = defaultdict(list)
        for antenna in self.antennas:
            antennas[antenna.frequency].append(antenna)

        # Loop the antennas of the same frequency
        for antenna_list in antennas.values():
            # Loop all possible pairs of antennas
            for left, right in itertools.permutations(antenna_list, 2):
                # Calculate the difference between the antennas
                diff_x = abs(left.x - right.x)
                diff_y = abs(left.y - right.y)

                # Depending on the position of the antennas, calculate
                # the antinodes in the direction of the antennas
                if left.x < right.x and left.y < right.y:
                    antinode_1 = [
                        Antinode(left.x - diff_x * i, left.y - diff_y * i)
                        for i in range(1, self.width)
                    ]
                    antinode_2 = [
                        Antinode(right.x + diff_x * i, right.y + diff_y * i)
                        for i in range(1, self.height)
                    ]
                elif left.x < right.x and left.y > right.y:
                    antinode_1 = [
                        Antinode(left.x - diff_x * i, left.y + diff_y * i)
                        for i in range(1, self.width)
                    ]
                    antinode_2 = [
                        Antinode(right.x + diff_x * i, right.y - diff_y * i)
                        for i in range(1, self.height)
                    ]
                elif left.x > right.x and left.y < right.y:
                    antinode_1 = [
                        Antinode(left.x + diff_x * i, left.y - diff_y * i)
                        for i in range(1, self.width)
                    ]
                    antinode_2 = [
                        Antinode(right.x - diff_x * i, right.y + diff_y * i)
                        for i in range(1, self.height)
                    ]
                else:
                    antinode_1 = [
                        Antinode(left.x + diff_x * i, left.y + diff_y * i)
                        for i in range(1, self.width)
                    ]
                    antinode_2 = [
                        Antinode(right.x - diff_x * i, right.y - diff_y * i)
                        for i in range(1, self.height)
                    ]

                # For the non-harmonic calculation, only consider the
                # first antinode
                if not with_harmonics:
                    antinodes.extend([antinode_1[0], antinode_2[0]])
                else:
                    antinodes.extend(antinode_1 + antinode_2)

                    # If there is more than one antenna of the same
                    # frequency, all antennas are also antinodes
                    if len(antenna_list) > 1:
                        antinodes.extend(
                            [
                                Antinode(antinode.x, antinode.y)
                                for antinode in antenna_list
                            ],
                        )

        # Filter out all antinodes that are not on the map
        antinodes = [
            antinode
            for antinode in antinodes
            if 0 <= antinode.x < self.width and 0 <= antinode.y < self.height
        ]
        return list(set(antinodes))


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    width = len(input_lines[0])
    height = len(input_lines)
    antennas = []
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if char == ".":
                continue
            else:
                antennas.append(Antenna(x, y, char))
    antenna_map = Map(width, height, antennas)
    anotinodes = antenna_map.find_antinodes()
    return len(anotinodes)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    width = len(input_lines[0])
    height = len(input_lines)
    antennas = []
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if char == ".":
                continue
            else:
                antennas.append(Antenna(x, y, char))
    antenna_map = Map(width, height, antennas)
    anotinodes = antenna_map.find_antinodes(with_harmonics=True)
    return len(anotinodes)


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_8.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
