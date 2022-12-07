# https://adventofcode.com/2021/day/4

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd


class Board:
    def __init__(self, numbers: list[list[int]]) -> None:
        self.numbers = pd.DataFrame(numbers)
        self.marks = pd.DataFrame(
            [
                [False, False, False, False, False],
                [False, False, False, False, False],
                [False, False, False, False, False],
                [False, False, False, False, False],
                [False, False, False, False, False],
            ]
        ).astype(bool)
        self.finished = False

    def draw(self, number: int) -> int | None:

        # Find the coordinates of the drawn number
        coordinates = [
            (x, self.numbers.columns[y])
            for x, y in zip(*np.where(self.numbers.values == number))
        ]
        if len(coordinates) == 0:
            return None

        # Mark the location
        y, x = coordinates[0]
        self.marks.iloc[y, x] = True

        # Check for the win condition
        if self.marks.all(axis=0).any() or self.marks.all(axis=1).any():
            numbers_marks_removed = self.numbers.where(self.marks == False, None)
            total = numbers_marks_removed.sum().sum()
            self.finished = True
            return total * number

        return None

    @classmethod
    def from_text(cls, text: list[str]) -> Board:
        numbers: list[list[int]] = []
        for line in text:
            numbers.append([int(value) for value in re.split(r"\s+", line)])
        return Board(numbers=numbers)


def process_game(moves: str, boards: list[Board]) -> int | None:
    for move in moves.split(","):
        number = int(move)
        for index, board in enumerate(boards):
            result = board.draw(number=number)
            if result is not None:
                print(
                    f"Found winning board: Board number {index} - Total score: {result}"
                )
                break
        else:
            continue
        break
    return result


def parse_input(input_lines: list[str]) -> tuple[str, list[Board]]:

    # Split the input
    moves = input_lines[0]
    board_contents = [line.strip() for line in input_lines[2:]]

    # Create a list of boards
    buffer: list[str] = []
    boards: list[Board] = []
    for line in board_contents:
        if line == "":
            boards.append(Board.from_text(buffer))
            buffer = []
        else:
            buffer.append(line)
    boards.append(Board.from_text(buffer))

    return moves, boards


def part_one(input_lines: list[str]) -> int:
    moves, boards = parse_input(input_lines)
    result = process_game(moves, boards)
    if result is None:
        raise Exception("No result found")
    return result


def part_two(input_lines: list[str]) -> int:
    moves, boards = parse_input(input_lines)

    for move in moves.split(","):
        number = int(move)
        for index, board in enumerate(boards):
            if board.finished:
                continue
            result = board.draw(number=number)
            if result is not None:
                print(
                    f"Found winning board: Board number {index} - Total score: {result}"
                )
    if result is None:
        raise Exception("No result found")
    return result


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_4.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
