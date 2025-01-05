# https://adventofcode.com/2021/day/21

from __future__ import annotations

import itertools
import math
import re
from abc import ABC, abstractmethod
from pathlib import Path


class Dice(ABC):
    rolled: int

    @abstractmethod
    def roll(self) -> int:
        ...

    @abstractmethod
    def roll_n_times(self, n_times: int) -> list[list[int]]:
        ...


class QuantumDice(Dice):
    def __init__(self) -> None:
        super().__init__()
        self.state = 0
        self.rolled = 0

    def roll(self) -> int:
        self.state += 1
        self.rolled += 1
        if self.state > 100:
            self.state = 1
        return self.state

    def roll_n_times(self, n_times: int) -> list[list[int]]:
        # TODO: Return a list of universes (all possible combinations)
        ...


class DeterministicDice(Dice):
    def __init__(self, n_sides: int = 100) -> None:
        super().__init__()
        self.state = 0
        self.rolled = 0
        self.sides = n_sides

    def roll_n_times(self, n_times: int) -> list[list[int]]:
        elements = list(range(1, 101)) * math.lcm(self.sides, 3, n_times)
        return [
            [
                sum([elements[i], elements[i + 1], elements[i + 2]])
                for i in range(0, n_times, 3)
            ]
        ]

    def roll(self) -> int:
        self.state += 1
        self.rolled += 1
        if self.state > 100:
            self.state = 1
        return self.state


class Board:
    def __init__(
        self, players: tuple[Player, Player], dice: Dice, win_score: int = 1000
    ) -> None:
        self.player_a, self.player_b = players
        self.active_player = self.player_a
        self.dice = dice
        self.n_rounds = 0
        self.win_score = win_score

    def play(self) -> tuple[list[int], list[int], list[int]]:
        # Return 3 lists; 2 with scores, one for each player; one with
        # the N dice rolls

        # Roll the dice N times, this returns a list of universes
        universes = self.dice.roll_n_times(self.win_score * 2)

        # Loop the universes
        results: tuple[list[int], list[int], list[int]] = ([], [], [])
        for dice_values in universes:

            # Player A
            dice_values_a = dice_values[::2]
            steps_a = [value % 10 for value in dice_values_a]
            positions_a = [
                10 if value % 10 == 0 else value % 10
                for value in itertools.accumulate([self.player_a.position, *steps_a])
            ]
            scores_a = list(itertools.accumulate(positions_a[1:]))

            # Player B
            dice_values_b = dice_values[1::2]
            steps_b = [value % 10 for value in dice_values_b]
            positions_b = [
                10 if value % 10 == 0 else value % 10
                for value in itertools.accumulate([self.player_b.position, *steps_b])
            ]
            scores_b = list(itertools.accumulate(positions_b[1:]))

            # Determine the winner
            els_a = [el >= self.win_score for el in scores_a].index(True)
            els_b = [el >= self.win_score for el in scores_b].index(True)

            if els_a <= els_b:
                results[0].append(scores_a[els_a])
                results[1].append(scores_b[els_a - 1])
                results[2].append((els_a * 2 + 1) * 3)

            else:
                results[0].append(scores_a[els_b - 1])
                results[1].append(scores_b[els_b])
                results[2].append((els_b * 2) * 3)

        return results


class Player:
    def __init__(self, name: str, starting_position: int) -> None:
        self.name = name
        self.score = 0
        self.position = starting_position

    def __repr__(self) -> str:
        return f"Player(name={self.name}, score={self.score}, position={self.position})"


def part_one(input_lines: list[str]) -> int:
    pattern = re.compile(r"Player \d starting position: (?P<starting_position>\d+)")
    starting_position_1 = re.search(pattern, input_lines[0]).group("starting_position")
    starting_position_2 = re.search(pattern, input_lines[1]).group("starting_position")

    player_1 = Player(name="A", starting_position=int(starting_position_1))
    player_2 = Player(name="B", starting_position=int(starting_position_2))

    board = Board(players=(player_1, player_2), dice=DeterministicDice())
    results = board.play()

    return min(results[0] + results[1]) * results[2][0]


def part_two(input_lines: list[str]) -> int:
    pattern = re.compile(r"Player \d starting position: (?P<starting_position>\d+)")
    starting_position_1 = re.search(pattern, input_lines[0]).group("starting_position")
    starting_position_2 = re.search(pattern, input_lines[1]).group("starting_position")

    player_1 = Player(name="A", starting_position=int(starting_position_1))
    player_2 = Player(name="B", starting_position=int(starting_position_2))

    board = Board(players=(player_1, player_2), dice=DeterministicDice())
    results = board.play()

    return results


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_21.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
