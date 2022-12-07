# https://adventofcode.com/2021/day/6

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


class LanternFish:
    def __init__(self, internal_timer: int = 8) -> None:
        self.internal_timer = internal_timer

    def progress_time(self) -> list[LanternFish]:
        if self.internal_timer == 0:
            self.internal_timer = 6
            return self.reproduce()
        else:
            self.internal_timer -= 1
            return []

    def reproduce(self, n_decendants: int = 1) -> list[LanternFish]:
        return [LanternFish() for _ in range(n_decendants)]


class LanternFishPopulation:
    def __init__(self, initial_state: str) -> None:
        self.original_population = pd.Series(
            [int(state) for state in initial_state.split(",")], dtype=int
        )
        self.generations: list[list[int]] = []

    @property
    def size(self) -> int:
        return int(
            len(self.original_population)
            + np.sum([generation[0] for generation in self.generations])
        )

    def progress_time(self):
        n_new_fish = self.original_population[self.original_population == 0].count()
        self.original_population -= 1

        for index, (n_children, age) in enumerate(self.generations):
            if age == 0:
                n_new_fish += n_children
                self.generations[index][1] = 6
            else:
                self.generations[index][1] -= 1
        if n_new_fish > 0:
            self.generations.append([n_new_fish, 8])

        self.original_population.loc[self.original_population == -1] = 6

    def simulate(self, n_timsteps: int) -> LanternFishPopulation:
        for _ in range(n_timsteps):
            self.progress_time()
        return self


def part_one(input_lines: list[str]) -> int:
    population = LanternFishPopulation(initial_state=input_lines[0])
    population.simulate(80)
    return population.size


def part_two(input_lines: list[str]) -> int:
    population = LanternFishPopulation(initial_state=input_lines[0])
    population.simulate(256)
    return population.size


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[2] / "data/year_2021/day_6.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
