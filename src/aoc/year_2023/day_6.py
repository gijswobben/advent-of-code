"""Assignment for day 6 of 2023 Advent of Code.

https://adventofcode.com/2023/day/6
"""

from functools import reduce
from pathlib import Path


class Race:

    """Represents a single race."""

    def __init__(self, time: int, record: int) -> None:
        """Single race instance.

        Args:
        ----
            time (int): The total duration of the race.
            record (int): The record distance.
        """
        self.time = time
        self.record = record

    def get_ways_to_win(self) -> list[int]:
        """Determine ways in which the race can be won.

        Returns
        -------
            list[int]: The different ways to win.
        """
        return [
            initial
            for initial in range(0, self.time)
            if (self.time - initial) * initial > self.record
        ]


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.
    """
    # Parse the input
    times = [int(m) for m in input_lines[0][5:].split()]
    records = [int(m) for m in input_lines[1][9:].split()]

    # Convert each combination of time and record to a race
    races = [Race(time=time, record=record) for time, record in zip(times, records)]

    # Determine the different ways to win
    ways_to_win = [len(race.get_ways_to_win()) for race in races]

    # Return the product of the ways to win
    return reduce(lambda x, y: x * y, ways_to_win)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.
    """
    # Parse the input
    time = int(input_lines[0][5:].replace(" ", ""))
    record = int(input_lines[1][9:].replace(" ", ""))

    # Convert to a race
    race = Race(time=time, record=record)

    # Determine the different ways to win
    return len(race.get_ways_to_win())


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_6.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
