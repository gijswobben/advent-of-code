# https://adventofcode.com/2022/day/15

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import z3
from scipy.spatial.distance import cityblock

INPUT_PATTERN = re.compile(
    r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)"
)


@dataclass(frozen=True)
class Position:
    """Class that represents a position on the grid."""

    x: int
    y: int


class Cave:
    """Represents the cave where the beacon should be found.

    Args:
        sensors (list[Sensor]): List of sensors that are spread out into
            the cave.
    """

    def __init__(self, sensors: list[Sensor]):
        self.sensors = sensors
        self.beacons: set[Position] = set(
            [
                Position(sensor.closest_beacon.x, sensor.closest_beacon.y)
                for sensor in sensors
            ]
        )

    def n_covered_by_sensor_at_y(self, y: int) -> int:
        """Find the number of positions covered by sensors at a certain
        value of Y.

        Args:
            y (int): The value of Y to search.

        Returns:
            int: The number of positions covered by sensors.
        """

        covered: list[Position] = []
        for sensor in self.sensors:

            # Calculate the distance between this sensor and the nearest
            # beacon
            distance = int(
                cityblock(
                    (sensor.x, sensor.y),
                    (sensor.closest_beacon.x, sensor.closest_beacon.y),
                )
            )

            # Start from right underneath/over the sensor on the desired
            # Y and keep moving out until the sensor no longer covers
            # this spot
            delta = 0
            while True:
                if (
                    int(cityblock((sensor.x, sensor.y), (sensor.x + delta, y)))
                    <= distance
                ):

                    # Symetrical so left and right are both covered by
                    # the sensor
                    covered.append(Position(sensor.x + delta, y))
                    covered.append(Position(sensor.x - delta, y))
                    delta += 1
                else:
                    break

        # Return the length of unique covered spots
        return len(set(covered))

    def find_beacon(self, width: int, height: int) -> Position:
        """Find the beacon on the grid.

        Finding the beacon is done by solving constraints. The
        constraints are defined as all the places the beacon cannot be;
        outside the search space, and within "range" of the sensor
        (where range is the manhattan distance between the sensor and
        the closest beacon).

        Args:
            width (int): Width of the search space.
            height (int): Height of the search space.

        Returns:
            Position: The position of the beacon.
        """

        solver = z3.Solver()
        x, y = z3.Ints("x y")

        # Add the search area boundaries as constraints
        solver.add(x >= 0, x <= width)
        solver.add(y >= 0, y <= height)

        # Loop all the sensors
        for sensor in self.sensors:

            # Calculate the distance between the sensor and the nearest
            # beacon
            distance = int(
                cityblock(
                    (sensor.x, sensor.y),
                    (sensor.closest_beacon.x, sensor.closest_beacon.y),
                )
            )

            # Take the absolute value of x and y (needed for manhathan
            # distance)
            absolute_distance_x = z3.If(x > sensor.x, x - sensor.x, sensor.x - x)
            absolute_distance_y = z3.If(y > sensor.y, y - sensor.y, sensor.y - y)

            # The point we're looking for should have a larger distance
            # than the distance to the nearest beacon
            solver.add((absolute_distance_x + absolute_distance_y) > distance)

        # Use to solver to find the solution
        solver.check()
        model = solver.model()

        # Return the found X and Y values
        return Position(int(model[x].as_long()), int(model[y].as_long()))

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Cave:
        """Create a Cave object from text input.

        Args:
            input_lines (list[str]): List of sensor/beacon pairs.

        Raises:
            Exception: Raised when an invalid line was encountered in
                the input.

        Returns:
            Cave: The cave object.
        """

        # Create a list of parsed sensors
        sensors: list[Sensor] = []
        for line in input_lines:

            # Match the pattern on the input string
            match = re.search(INPUT_PATTERN, line)
            if match is None:
                raise Exception("Invalid line")

            # Create a new sensor/beacon pair from the input string
            sensor = Sensor(
                position=Position(
                    x=int(match["sensor_x"]),
                    y=int(match["sensor_y"]),
                ),
                closest_beacon=Position(
                    x=int(match["beacon_x"]),
                    y=int(match["beacon_y"]),
                ),
            )
            sensors.append(sensor)

        # Create the cave with the sensors and beacons
        return Cave(sensors=sensors)


class Sensor:
    """Represents a single sensor.

    Each sensor has one beacon that is closest.

    Args:
        position (Position): The position of this sensor.
        closest_beacon (Beacon): The beacon that is closest to this
            sensor.
    """

    def __init__(self, position: Position, closest_beacon: Position) -> None:
        self.position = position
        self.closest_beacon = closest_beacon

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    @property
    def min_distance_to_beacon(self) -> int:
        """The manhathan distance between this sensor and the nearest
        beacon."""

        return cityblock(
            (self.x, self.y), (self.closest_beacon.x, self.closest_beacon.y)
        )

    def __repr__(self) -> str:
        return f"Sensor<{self.x}, {self.y}>"


def part_one(input_lines: list[str], y: int = 2000000) -> int:

    # Parse the input as a cave
    cave = Cave.from_text(input_lines)

    # Count the number of covered spaces at a certain position of Y
    total = cave.n_covered_by_sensor_at_y(y=y)

    # Remove any known beacons
    total -= len([beacon for beacon in set(cave.beacons) if beacon.y == y])

    return total


def part_two(
    input_lines: list[str], width: int = 4000000, height: int = 4000000
) -> int:

    # Parse the input as a cave
    cave = Cave.from_text(input_lines)

    # Find the beacon within the search space
    position = cave.find_beacon(width=width, height=height)

    # Return the x position * 4000000 + the y position as the solution
    return position.x * 4000000 + position.y


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_15.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
