# https://adventofcode.com/2022/day/16

from __future__ import annotations

import functools
import itertools
import re
from collections import deque
from pathlib import Path

import networkx as nx

VALVE_PATTERN = re.compile(
    r"Valve (?P<valve_name>\w+) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<other_valves>.+)"
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

        # Create a graph based on the layout of the valves. This graph
        # will be used to find paths between the caves
        self.graph = nx.Graph()
        for valve in self.valves.values():
            self.graph.add_edges_from(
                [(valve, self.valves[other]) for other in valve.tunnels]
            )

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Cave:
        """Create a new Cave object from text input.

        Args:
            input_lines (list[str]): The lines of text containing
                definitions of the valves.

        Raises:
            Exception: Raised when an invalid input line was discovered.

        Returns:
            Cave: The resulting Cave object.
        """

        # Create a list of Valves
        valves: list[Valve] = []
        for line in input_lines:

            match = re.search(VALVE_PATTERN, line)
            if match is None:
                raise Exception("Invalid input")
            else:
                valves.append(
                    Valve(
                        name=match.group("valve_name"),
                        flow_rate=int(
                            match.group("flow_rate"),
                        ),
                        tunnels=[
                            tunnel.strip()
                            for tunnel in match.group("other_valves").split(",")
                        ],
                    )
                )

        return Cave(valves=valves)

    def list_all_paths(self, start: Valve, time: int) -> list[CavePath]:
        """List all possible paths through the cave system, from a
        particular start valve.

        Args:
            start (Valve): The valve to start from.
            time (int): The time limit for moving through the caves.

        Returns:
            list[CavePath]: List of discovered paths.
        """

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
            if source != target
        }

        # Create a queue of paths to further explore
        queue: deque[CavePath] = deque([CavePath(time=time, visited=[start])])
        complete_paths: list[CavePath] = []
        while queue:

            # Get the first item in the queue (FIFO)
            path = queue.popleft()
            complete_paths.append(path)

            # Skip this path if there is not enough time to explore
            # additional valves
            if path.time <= 3:
                continue

            # Keep discovering new paths if there is enough time to move
            # and open, and the valve adds value and the valve isn't
            # open yet
            new_paths = []
            targets = [
                valve
                for valve in significant_valves
                if valve not in path.visited
                and path.time > (distances[(path.visited[-1], valve)] + 2)
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
                queue.extend(new_paths)

            # This was the last valve in the search, stop searching
            # this path
            else:
                complete_paths.append(path)

        return complete_paths

    def calculate_max_pressure_released(
        self, total_time: int, n_actors: int = 1
    ) -> int:
        """Calculate the maximum pressure that N actors can release
        within a certain amount of time.

        Args:
            total_time (int, optional): The total time the actors can
                move.
            n_actors (int, optional): The number of actors in the cave
                system. Defaults to 1.

        Returns:
            int: The maximum total pressure released.
        """

        # All paths that fit in the time
        all_paths = self.list_all_paths(start=self.valves["AA"], time=total_time)

        # Sort the paths based on highest pressure released
        all_paths.sort(key=lambda p: p.total_pressure_released, reverse=True)

        # If there is only 1 actor, get the path with the highest
        # pressure released (first item of the already sorted list)
        if n_actors == 1:
            return all_paths[0].total_pressure_released

        # If there are more actors, find the optimal non-overlapping set
        # of paths
        else:

            # Keep track of the combination that results in the highest
            # pressure released and loop all combinations of paths
            max_pressure_released = 0
            for combination in itertools.combinations(all_paths, n_actors):

                # Sum the released pressure for this combination
                total_pressure = sum(
                    [valve.total_pressure_released for valve in combination]
                )

                # Only proceed if this combination results in a better
                # pressure release
                if total_pressure <= max_pressure_released:
                    continue

                # Create a set of visited nodes, excluding the start
                # node, for every actor and make sure they don't overlap
                sets = [set(valve.visited[1:]) for valve in combination]
                if (
                    len(functools.reduce(lambda m, n: set.intersection(m, n), sets))
                    == 0
                ):
                    max_pressure_released = total_pressure

            return max_pressure_released


def part_one(input_lines: list[str]) -> int:

    # Parse the input into a cave system with valves
    cave = Cave.from_text(input_lines)

    # Calculate the total pressure that can be released
    return cave.calculate_max_pressure_released(total_time=30, n_actors=1)


def part_two(input_lines: list[str]) -> int:

    # Parse the input into a cave system with valves
    cave = Cave.from_text(input_lines)

    # Calculate the total pressure that can be released
    return cave.calculate_max_pressure_released(total_time=26, n_actors=2)


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
