# https://adventofcode.com/2021/day/1

from io import StringIO
from pathlib import Path

import pandas as pd


def part_one(input_lines: list[str]) -> int:
    """Count the number of lines that show an increment.

    Args:
        input_lines (list[str]): The input as a list of measurements
            (strings).

    Returns:
        int: The number of increments.
    """

    # Convert the input to a series
    series = pd.read_csv(StringIO("\n".join(input_lines)), header=None)[0]

    # Select rows where the difference between this row and the previous is
    # larger than 0, and count the remaining rows
    series = series[(series.diff() > 0)]

    return series.count()


def part_two(input_lines: list[str]) -> int:
    """Count the number of lines that show an increment in groups of 3.

    Args:
        input_lines (list[str]): The input as a list of measurements
            (strings).

    Returns:
        int: The number of increments.
    """

    # Convert the input to a dataframe
    df = pd.read_csv(StringIO("\n".join(input_lines)), header=None)

    # Create shifted fields
    df[1] = df[0].shift(-1)
    df[2] = df[0].shift(-2)

    # Drop rows with empty values
    df = df.dropna(axis=0, how="any")

    # Add the total column
    df["sum"] = df[[0, 1, 2]].sum(axis=1)

    # Select rows where the difference between this row and the previous is
    # larger than 0, and count the remaining rows
    selection = df[(df["sum"].diff() > 0)]
    return selection["sum"].count()


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[2] / "data/year_2021/day_1.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
