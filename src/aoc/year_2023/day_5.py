"""Assignment for day 5 of 2023 Advent of Code.

https://adventofcode.com/2023/day/5
"""

from __future__ import annotations

import itertools
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import networkx as nx  # type: ignore
import portion
from rich import print


@dataclass
class Mapping:
    source_key: str | None = None
    destination_key: str | None = None
    destination_range_start: int | None = None
    source_range_start: int | None = None
    range_length: int | None = None

    @property
    def range(self) -> portion.Interval:
        return portion.closedopen(
            self.source_range_start,
            self.source_range_start + self.range_length,
        )

    def map_value(self, value: int) -> int:
        return self.destination_range_start + (value - self.source_range_start)


class Almanac:
    def __init__(self, definition: list[str]) -> None:
        # Keep track of the different relations to figure out how to map
        # one type into another in a generic way
        self.dag = nx.DiGraph()

        # Use the rest of the definition to parse the mappings
        mapping_pattern = re.compile(r"(?P<source>\w+)-to-(?P<destination>\w+)\s*map:")
        found_maps = []
        source: str | None = None
        destination: str | None = None
        for line in definition[1:]:
            # Skip blank lines
            if not line:
                continue

            # New mapping started
            elif match := mapping_pattern.match(line):
                # Store the mapping in the DAG
                if match.group("source") not in self.dag:
                    self.dag.add_node(match.group("source"))
                if match.group("destination") not in self.dag:
                    self.dag.add_node(match.group("destination"))
                self.dag.add_edge(match.group("source"), match.group("destination"))

                # Store the mapping in the list of found maps
                source = match.group("source")
                destination = match.group("destination")

            # Numbers related to the current mapping
            elif line[0].isdigit():
                numbers = [int(m) for m in re.findall(r"\d+", line)]
                found_maps.append(
                    Mapping(
                        source_key=source,
                        destination_key=destination,
                        destination_range_start=numbers[0],
                        source_range_start=numbers[1],
                        range_length=numbers[2],
                    ),
                )

        # Create a dictionary that maps source, destination combinations
        # to a list of mapping objects
        self._maps: defaultdict[str, defaultdict[str, list[Mapping]]] = defaultdict(
            lambda: defaultdict(list),
        )
        for mapping in found_maps:
            self._maps[mapping.source_key][mapping.destination_key].append(mapping)

    def _find_path(self, source: str, target: str) -> list[str]:
        # Find the shortest path from source to destination through the
        # DAG
        return nx.shortest_path(self.dag, source, target)

    def map(
        self,
        range_object: portion.Interval,
        source_key: str = "seed",
        destination_key: str = "location",
    ) -> list[portion.Interval]:
        # Create an IntervalDict where the keys are Interval objects and
        # the values are mapping objects (or None). IntervalDict
        # automatically split keys when you add a new key that overlaps
        mapping: portion.IntervalDict[
            portion.Interval,
            None | Mapping,
        ] = portion.IntervalDict(
            {range_object: None},
        )

        # Determine the steps to take for converting soil to location
        path = self._find_path(source_key, destination_key)

        # For each step in the path
        for source, destination in itertools.pairwise(path):
            # If a mapping exists
            if source in self._maps and destination in self._maps[source]:
                # Apply the mappings to the mapping dict
                for mapping_object in self._maps[source][destination]:
                    for key in mapping.keys():
                        mapping[key & mapping_object.range] = mapping_object

                # Apply mappings to the applicable ranges
                mapping = portion.IntervalDict(
                    {
                        key
                        if value is None
                        else key.replace(
                            lower=lambda lower: value.map_value(lower),
                            upper=lambda upper: value.map_value(upper),
                        ): None
                        for key, value in mapping.items()
                    },
                )

        return list(mapping.keys())


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.
    """
    # Extract the seeds
    seeds = [portion.singleton(int(m)) for m in re.findall(r"\d+", input_lines[0])]

    # Parse the almanac
    almanac = Almanac(input_lines)

    # Convert each seed to a location
    locations: list[int] = [almanac.map(seed) for seed in seeds]

    # Get the lowest location number
    return min(
        [location.lower for location in itertools.chain.from_iterable(locations)],
    )


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.
    """
    # Extract the seeds
    seed_definitions = [int(m) for m in re.findall(r"\d+", input_lines[0])]
    seed_ranges: list[portion.Interval] = [
        portion.closedopen(
            seed_definitions[index],
            seed_definitions[index] + seed_definitions[index + 1],
        )
        for index in range(0, len(seed_definitions), 2)
    ]

    # Parse the almanac
    almanac = Almanac(input_lines)

    # Convert each seed range to a range of locations
    locations: list[portion.Interval] = [
        almanac.map(seed_range) for seed_range in seed_ranges
    ]

    # Get the lowest location number
    return min(
        [location.lower for location in itertools.chain.from_iterable(locations)],
    )


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_5.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
