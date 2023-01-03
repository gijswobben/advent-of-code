# https://adventofcode.com/2022/day/16

from __future__ import annotations

import itertools
import re
from collections import deque
from pathlib import Path
from typing import Any

import networkx as nx

VALVE_PATTERN = re.compile(
    r"Valve (?P<valve_name>\w+) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<other_valves>.+)"
)


def all_combinations(any_list: list) -> itertools.chain[tuple[Any, ...]]:
    return itertools.chain.from_iterable(
        itertools.combinations(any_list, i + 1) for i in range(len(any_list))
    )


class Valve:
    """Represents a single Valve that can be opened to release pressure.

    Args:
        name (str): Name of this valve (for reference).
        flow_rate (int): The amount of pressure released at every
            timestep.
        tunnels (list[str]): List of names of connected valves.
    """

    def __init__(self, name: str, flow_rate: int, tunnels: list[str]) -> None:
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels
        self.is_open = False

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}<name={self.name}, flow_rate={self.flow_rate}>"
        )


class CavePath:
    """Path from cave to cave.

    Keeps track of the pressure released and the already visited caves.

    Args:
        time (int): The time remaining on the clock.
        visited (list[Valve]): List of already visited Valves.
        total_pressure_released (int): Already released pressure.
            Defaults to 0.
    """

    def __init__(
        self, time: int, visited: list[Valve], total_pressure_released: int = 0
    ) -> None:
        self.time = time
        self.visited = visited
        self.total_pressure_released = total_pressure_released

    def add(self, valve: Valve, time: int):
        """Add a Valve to this path.

        Args:
            valve (Valve): The valve to add to the path.
            time (int): The time remaining after opening the target
                valve.
        """

        self.visited.append(valve)
        self.time = time

    def copy(self) -> CavePath:
        """Create a copy from this path.

        Returns:
            CavePath: A copy of this CavePath.
        """
        return CavePath(
            time=self.time,
            visited=self.visited.copy(),
            total_pressure_released=self.total_pressure_released,
        )

    def __repr__(self) -> str:
        return f"Path<pressure: {self.total_pressure_released}, visited: {', '.join(str(v) for v in self.visited)}>"


class Cave:
    """Represents a cave in the cave system.

    Args:
        valves (list[Valve]): List of valves in the cave system.
    """

    def __init__(self, valves: list[Valve]) -> None:
        self.valves: dict[str, Valve] = {valve.name: valve for valve in valves}

        # Create a graph based on the layout of the valves
        self.graph = nx.Graph()
        for valve in self.valves.values():
            self.graph.add_edges_from(
                [(valve, self.valves[other]) for other in valve.tunnels]
            )

    def release_pressure(self, total_time: int = 30) -> int:

        # Pre-calculate all the distances between node pairs for speed
        distances: dict[tuple[Valve, Valve], int] = {
            (source, target): nx.shortest_path_length(self.graph, source, target)
            for source, target in itertools.product(
                [
                    valve
                    for valve in self.valves.values()
                    if valve.flow_rate > 0 or valve.name == "AA"
                ],
                [
                    valve
                    for valve in self.valves.values()
                    if valve.flow_rate > 0 or valve.name == "AA"
                ],
            )
        }

        def _recurse(
            current_valve: Valve,
            open_valves: list[Valve],
            time_left: int,
        ) -> int:

            # Calculate the pressure released from all open valves
            pressure_released = sum(
                [open_valve.flow_rate for open_valve in open_valves]
            )

            # Stop searching if there is no time left to move and open a
            # valve
            if time_left <= 1:
                return pressure_released

            # Loop all valves and calculate the potential yield from
            # moving to that valve
            potential_yields: list[tuple[Valve, int]] = []
            for valve in self.valves.values():

                # Skip open valves or 0 flow rate valves
                if valve in open_valves or valve.flow_rate == 0:
                    continue

                # Get the arrival time if we choose to travel to this
                # valve
                time_left_at_arrival = time_left - distances[(current_valve, valve)]
                if time_left_at_arrival <= 1:
                    continue

                # Calculate the potential yield from opening the target
                # valve (takes 1 minute to open)
                potential_yield = pressure_released * (
                    distances[(current_valve, valve)]
                ) + _recurse(
                    valve,
                    open_valves=[*open_valves, valve],
                    time_left=time_left_at_arrival - 1,
                )
                potential_yields.append((valve, potential_yield))

            # No more moves (e.g. every valve is open)
            if len(potential_yields) == 0:
                return pressure_released + _recurse(
                    current_valve=current_valve,
                    open_valves=open_valves,
                    time_left=time_left - 1,
                )

            # Get the next best option by sorting the valves by
            # potential yield
            else:
                next_valve = sorted(
                    potential_yields, key=lambda row: row[1], reverse=True
                )[0][1]
                return pressure_released + next_valve

        return _recurse(
            current_valve=self.valves["AA"], time_left=total_time, open_valves=[]
        )

    def release_pressure_with_elephant(
        self, total_time: int = 26, n_actors: int = 2
    ) -> int:
        def find_paths(start: Valve, time_remaining: int):

            # Filter to only valves that have a flow rate
            significant_valves = [
                valve
                for valve in self.valves.values()
                if valve.flow_rate > 0 or valve == start
            ]

            # Pre-calculate all the distances between node pairs for
            # speed
            distances: dict[tuple[Valve, Valve], int] = {
                (source, target): nx.shortest_path_length(self.graph, source, target)
                for source, target in itertools.product(
                    significant_valves, significant_valves
                )
            }

            stack: deque[CavePath] = deque([CavePath(time=total_time, visited=[start])])
            complete_paths: list[CavePath] = []
            while stack:
                path = stack.popleft()

                complete_paths.append(path)

                if path.time <= 3:
                    continue

                new_paths = []

                # Keep moving if there is enough time to move and open and
                # the valve adds value and the valve isn't open yet
                targets = [
                    valve
                    for valve in significant_valves
                    if valve not in path.visited
                    and time_remaining > (distances[(path.visited[-1], valve)] + 1)
                ]

                # Go over all possible targets and create a new "path"
                # ending in the target
                for target in targets:
                    new_path = path.copy()
                    new_path.add(
                        valve=target,
                        time=path.time - (distances[(path.visited[-1], target)] + 1),
                    )
                    new_path.total_pressure_released += (
                        path.time - (distances[(path.visited[-1], target)] + 1)
                    ) * target.flow_rate
                    new_paths.append(new_path)

                # Add the newly discovered options to the stack
                if new_paths:
                    stack.extend(new_paths)

                # This was the last valve in the search, stop searching
                # this path
                else:
                    complete_paths.append(path)

            return complete_paths

        # All paths that fit in the time
        all_paths = find_paths(start=self.valves["AA"], time_remaining=total_time)

        # Sort the paths based on highest pressure released
        all_paths.sort(key=lambda p: p.total_pressure_released, reverse=True)

        # Loop over the sorted list of paths
        max_pressure_released = 0
        for i, path_a in enumerate(all_paths):

            x = set(tuple(path_a.visited[1:]))

            # Go over the rest of the list
            for path_b in all_paths[i + 1 :]:
                if (
                    path_a.total_pressure_released + path_b.total_pressure_released
                    <= max_pressure_released
                ):
                    break

                y = set(tuple(path_b.visited[1:]))

                if len(set.intersection(x, y)) == 0:
                    if (
                        path_a.total_pressure_released + path_b.total_pressure_released
                        > max_pressure_released
                    ):
                        max_pressure_released = (
                            path_a.total_pressure_released
                            + path_b.total_pressure_released
                        )

        return max_pressure_released


def part_one(input_lines: list[str]) -> int:
    valves: list[Valve] = []
    for line in input_lines:
        match = re.search(VALVE_PATTERN, line)
        if match is None:
            raise Exception("Invalid input")
        else:
            valve = Valve(
                name=match.group("valve_name"),
                flow_rate=int(
                    match.group("flow_rate"),
                ),
                tunnels=[
                    tunnel.strip() for tunnel in match.group("other_valves").split(",")
                ],
            )
            valves.append(valve)

    cave = Cave(valves=valves)

    total_pressure_released = cave.release_pressure()
    return total_pressure_released


def part_two(input_lines: list[str]) -> int:
    valves: list[Valve] = []
    for line in input_lines:
        match = re.search(VALVE_PATTERN, line)
        if match is None:
            raise Exception("Invalid input")
        else:
            valve = Valve(
                name=match.group("valve_name"),
                flow_rate=int(
                    match.group("flow_rate"),
                ),
                tunnels=[
                    tunnel.strip() for tunnel in match.group("other_valves").split(",")
                ],
            )
            valves.append(valve)

    cave = Cave(valves=valves)

    total_pressure_released = cave.release_pressure_with_elephant()
    return total_pressure_released


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_16.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
