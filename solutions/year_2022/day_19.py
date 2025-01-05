# https://adventofcode.com/2022/day/19

from __future__ import annotations

import functools
import re
from abc import ABC
from pathlib import Path
from typing import Type

import z3

BLUEPRINT_PATTERN = re.compile(
    r"Blueprint (?P<blueprint_id>\d+): Each ore robot costs (?P<ore_robot_cost>\d+) ore\. Each clay robot costs (?P<clay_robot_cost>\d+) ore\. Each obsidian robot costs (?P<obsidian_robot_cost_ore>\d+) ore and (?P<obsidian_robot_cost_clay>\d+) clay\. Each geode robot costs (?P<geode_robot_cost_ore>\d+) ore and (?P<geode_robot_cost_obsidian>\d+) obsidian\."
)


class Resource(ABC):
    ...


class Ore(Resource):
    ...


class Clay(Resource):
    ...


class Obsidian(Resource):
    ...


class Geode(Resource):
    ...


class Robot(ABC):
    ...


class OreRobot(Robot):
    ...


class ClayRobot(Robot):
    ...


class ObsidianRobot(Robot):
    ...


class GeodeRobot(Robot):
    ...


class Blueprint:
    """Represents a blueprint of producing robots.

    Args:
        identifier (int): ID of this blueprint.
        ore_robot_cost (int): Costs for this robot.
        clay_robot_cost (int): Costs for this robot.
        obsidian_robot_cost_ore (int): Costs for this robot.
        obsidian_robot_cost_clay (int): Costs for this robot.
        geode_robot_cost_ore (int): Costs for this robot.
        geode_robot_cost_obsidian (int): Costs for this robot.
    """

    def __init__(
        self,
        identifier: int,
        ore_robot_cost: int,
        clay_robot_cost: int,
        obsidian_robot_cost_ore: int,
        obsidian_robot_cost_clay: int,
        geode_robot_cost_ore: int,
        geode_robot_cost_obsidian: int,
    ) -> None:
        self.identifier = identifier

        # Map the costs to robots
        self.robot_costs: dict[Type[Robot], dict[Type[Resource], int]] = {
            OreRobot: {
                Ore: ore_robot_cost,
            },
            ClayRobot: {Ore: clay_robot_cost},
            ObsidianRobot: {
                Ore: obsidian_robot_cost_ore,
                Clay: obsidian_robot_cost_clay,
            },
            GeodeRobot: {
                Ore: geode_robot_cost_ore,
                Obsidian: geode_robot_cost_obsidian,
            },
        }

    def find_optimal_geode_production(self, time: int) -> int:
        """Find the optimal number of geodes that can be produced using]
        this blueprint.

        Args:
            time (int): The time to use for producing geodes.

        Returns:
            int: The optimal number of geodes that can be produced.
        """

        # Add one for time = 0
        _time = time + 1
        time_range = range(1, _time)

        # Create a solver that will optimize the number of geodes
        # produced
        solver = z3.Optimize()

        # Keep track of the inventory per resource at every timestep
        inventory: dict[Type[Resource], list[z3.ArithRef]] = {
            Ore: z3.Ints(" ".join([f"ore_{i}" for i in range(_time)])),
            Clay: [z3.Int(f"clay_{i}") for i in range(_time)],
            Obsidian: [z3.Int(f"obsidian_{i}") for i in range(_time)],
            Geode: [z3.Int(f"geode_{i}") for i in range(_time)],
        }

        # Keep track of the number of robots at every timestep
        robots: dict[Type[Robot], list[z3.Int]] = {
            OreRobot: [z3.Int(f"ore_robot_{i}") for i in range(_time)],
            ClayRobot: [z3.Int(f"clay_robot_{i}") for i in range(_time)],
            ObsidianRobot: [z3.Int(f"obsidian_robot_{i}") for i in range(_time)],
            GeodeRobot: [z3.Int(f"geode_robot_{i}") for i in range(_time)],
        }

        # Keep track of how may robots have been bought at every
        # timestep
        buy_history: dict[Type[Robot], list[z3.Int]] = {
            OreRobot: [z3.Int(f"buy_ore_robot_{i}") for i in range(_time)],
            ClayRobot: [z3.Int(f"buy_clay_robot_{i}") for i in range(_time)],
            ObsidianRobot: [z3.Int(f"buy_obsidian_robot_{i}") for i in range(_time)],
            GeodeRobot: [z3.Int(f"buy_geode_robot_{i}") for i in range(_time)],
        }

        # The inventory at any moment in time, is the previous amount +
        # the number of robots at the previous timestep - the spent
        # amount in the past
        for t in time_range:
            for resource_type, robot_type in zip(inventory.keys(), robots.keys()):
                solver.add(
                    inventory[resource_type][t]
                    == inventory[resource_type][t - 1]
                    + robots[robot_type][t - 1]
                    - (buy_history[robot_type][t - 1])
                    * self.robot_costs[OreRobot].get(resource_type, 0)
                    - (buy_history[ClayRobot][t - 1])
                    * self.robot_costs[ClayRobot].get(resource_type, 0)
                    - (buy_history[ObsidianRobot][t - 1])
                    * self.robot_costs[ObsidianRobot].get(resource_type, 0)
                    - (buy_history[GeodeRobot][t - 1])
                    * self.robot_costs[GeodeRobot].get(resource_type, 0)
                )

        # A new robot can only be bought when there are enough resources
        # to do so
        for t in time_range:

            for robot_type, required_resources in self.robot_costs.items():
                for required_resource, required_amount in required_resources.items():

                    # Inventory for a resource should be bigger than the
                    # required amount to build this robot
                    solver.add(
                        inventory[required_resource][t]
                        >= buy_history[robot_type][t] * required_amount
                    )

        # The total number of robots at any time, is the previous number
        # + the robots that are build in the previous timestep
        for t in time_range:

            for robot_type in robots.keys():
                solver.add(
                    robots[robot_type][t]
                    == robots[robot_type][t - 1] + buy_history[robot_type][t - 1]
                )

        # Resources can never go negative
        for t in time_range:
            for resource_type in inventory.keys():
                solver.add(inventory[resource_type][t] >= 0)

        # The number of robots can never go negative
        for t in time_range:
            for robot_type in robots.keys():
                solver.add(robots[robot_type][t] >= 0)

        # We can build at most 1 robot at a time
        for t in time_range:
            for robot_type in robots.keys():
                solver.add(
                    buy_history[robot_type][t] >= 0, buy_history[robot_type][t] <= 1
                )

        # Buy at most 1 robot of any type per timestep
        for t in time_range:
            solver.add(
                buy_history[OreRobot][t]
                + buy_history[ClayRobot][t]
                + buy_history[ObsidianRobot][t]
                + buy_history[GeodeRobot][t]
                <= 1
            )

        # Initial inventory
        for resource_type in inventory.keys():
            solver.add(inventory[resource_type][0] == 0)

        # Initial buy history (cannot buy at t=0)
        for robot_type in robots.keys():
            solver.add(buy_history[robot_type][0] == 0)

        # Initial set of robots
        solver.add(robots[OreRobot][0] == 1)
        solver.add(robots[ClayRobot][0] == 0)
        solver.add(robots[ObsidianRobot][0] == 0)
        solver.add(robots[GeodeRobot][0] == 0)

        # Solve the problem
        solver.maximize(inventory[Geode][time])
        solver.check()
        model = solver.model()
        return int(model[inventory[Geode][time]].as_long())

    @classmethod
    def from_string(cls, input_string: str) -> Blueprint:
        """Parse text into a Blueprint object.

        Args:
            input_string (str): The blueprint definition.

        Raises:
            Exception: Raised when the blueprint isn't valid.

        Returns:
            Blueprint: The parsed blueprint object.
        """

        match = re.search(BLUEPRINT_PATTERN, input_string)
        if match is None:
            raise Exception("Invalid blueprint")

        blueprint_id = match.group("blueprint_id")
        ore_robot_cost = match.group("ore_robot_cost")
        clay_robot_cost = match.group("clay_robot_cost")
        obsidian_robot_cost_ore = match.group("obsidian_robot_cost_ore")
        obsidian_robot_cost_clay = match.group("obsidian_robot_cost_clay")
        geode_robot_cost_ore = match.group("geode_robot_cost_ore")
        geode_robot_cost_obsidian = match.group("geode_robot_cost_obsidian")

        return Blueprint(
            identifier=int(blueprint_id),
            ore_robot_cost=int(ore_robot_cost),
            clay_robot_cost=int(clay_robot_cost),
            obsidian_robot_cost_ore=int(obsidian_robot_cost_ore),
            obsidian_robot_cost_clay=int(obsidian_robot_cost_clay),
            geode_robot_cost_ore=int(geode_robot_cost_ore),
            geode_robot_cost_obsidian=int(geode_robot_cost_obsidian),
        )


def part_one(input_lines: list[str]) -> int:

    # Parse the blueprints
    blueprints: list[Blueprint] = []
    for line in input_lines:
        blueprints.append(Blueprint.from_string(line))

    # Make a list of quality scores
    quality_scores: list[int] = []
    for blueprint in blueprints:
        geodes_produced = blueprint.find_optimal_geode_production(time=24)
        quality_scores.append(geodes_produced * blueprint.identifier)
    return sum(quality_scores)


def part_two(input_lines: list[str]) -> int:

    # Parse the blueprints
    blueprints: list[Blueprint] = []
    for line in input_lines:
        blueprints.append(Blueprint.from_string(line))

    # Calculate the geodes for the first 3 blueprints
    total_geodes: list[int] = []
    for blueprint in blueprints[:3]:
        geodes_produced = blueprint.find_optimal_geode_production(time=32)
        total_geodes.append(geodes_produced)

    # Multiply all geodes produced
    return functools.reduce(lambda a, b: a * b, total_geodes)


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_19.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
