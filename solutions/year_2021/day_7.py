# https://adventofcode.com/2021/day/7

from pathlib import Path

import numpy as np
import pandas as pd


def align_crabs(input_positions: str):
    positions = pd.DataFrame(
        {"original_positions": [int(state) for state in input_positions.split(",")]}
    )

    min_position = min(positions["original_positions"])
    max_position = max(positions["original_positions"])

    cost_matrix: list[tuple[int, int]] = []
    for position in range(min_position, max_position + 1):
        cost_matrix.append(
            (position, (positions["original_positions"] - position).abs().sum())
        )
    costs = pd.DataFrame(cost_matrix, columns=["position", "cost"])

    min_cost = costs["cost"].min()
    optimal_position = costs.loc[costs["cost"].idxmin(), "position"]
    return optimal_position, min_cost


def align_crabs_alt(input_positions: str):
    positions = pd.DataFrame(
        {"original_positions": [int(state) for state in input_positions.split(",")]}
    )

    min_position = min(positions["original_positions"])
    max_position = max(positions["original_positions"])

    cost_matrix: list[tuple[int, int]] = []
    for position in range(min_position, max_position + 1):
        cost = (
            (positions["original_positions"] - position)
            .abs()
            .apply(lambda steps: np.sum(range(steps + 1)))
            .sum()
        )
        cost_matrix.append((position, cost))
    costs = pd.DataFrame(cost_matrix, columns=["position", "cost"])

    min_cost = costs["cost"].min()
    optimal_position = costs.loc[costs["cost"].idxmin(), "position"]
    return optimal_position, min_cost


def part_one(input_lines: list[str]) -> int:
    _, min_cost = align_crabs(input_positions=input_lines[0])
    return min_cost


def part_two(input_lines: list[str]) -> int:
    _, min_cost = align_crabs_alt(input_positions=input_lines[0])
    return min_cost


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_7.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
