# https://adventofcode.com/2022/day/2

from enum import IntEnum
from pathlib import Path
from typing import cast


class Gesture(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class GameOutcome(IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6


INPUT_MAPPING: dict[str, Gesture] = {
    "A": Gesture.ROCK,
    "B": Gesture.PAPER,
    "C": Gesture.SCISSORS,
    "X": Gesture.ROCK,
    "Y": Gesture.PAPER,
    "Z": Gesture.SCISSORS,
}

OUTCOME_MAPPING: dict[str, GameOutcome] = {
    "X": GameOutcome.LOSE,
    "Y": GameOutcome.DRAW,
    "Z": GameOutcome.WIN,
}


BEATS_MAPPING: dict[Gesture, Gesture] = {
    Gesture.ROCK: Gesture.SCISSORS,
    Gesture.SCISSORS: Gesture.PAPER,
    Gesture.PAPER: Gesture.ROCK,
}


class Game:
    """Class to represent a single game of Rock-Paper-Scissors.

    The class expects at least an input gesture and a response gesture
    or game outcome. Depending on which input is provided it will
    determine the corresponding game outcome or response move.

    Args:
        input_gesture (Gesture): The input gesture.
        response_gesture (Gesture | None, optional): An optional
            response gesture, which will be determined automatically if
            the game_outcome is provided. Defaults to None.
        game_outcome (GameOutcome | None, optional): An optional game
            outcome, which will be determined automatically if the
            response_gesture is provided. Defaults to None.
    """

    def __init__(
        self,
        input_gesture: Gesture,
        response_gesture: Gesture | None = None,
        game_outcome: GameOutcome | None = None,
    ) -> None:
        self.input_gesture = input_gesture
        if response_gesture is None and game_outcome is not None:
            self.response_gesture = self.determine_response(input_gesture, game_outcome)
            self.game_outcome = game_outcome
        elif response_gesture is not None and game_outcome is None:
            self.response_gesture = response_gesture
            self.game_outcome = self.determine_outcome(input_gesture, response_gesture)
        else:
            self.response_gesture = cast(Gesture, response_gesture)
            self.game_outcome = cast(GameOutcome, game_outcome)

    def determine_outcome(
        self, input_gesture: Gesture, response_gesture: Gesture
    ) -> GameOutcome:
        """Determine the game outcome based on the input and response
        gestures.

        Args:
            input_gesture (Gesture): The input gesture.
            response_gesture (Gesture): The response gesture.

        Returns:
            GameOutcome: The game outcome.
        """
        if input_gesture == response_gesture:
            return GameOutcome.DRAW
        if response_gesture == BEATS_MAPPING[input_gesture]:
            return GameOutcome.WIN
        else:
            return GameOutcome.LOSE

    def determine_response(
        self, input_gesture: Gesture, game_outcome: GameOutcome
    ) -> Gesture:
        """Determine the response required to achieve the desired game
        outcome.

        Args:
            input_gesture (Gesture): The input gesture to respond to.
            game_outcome (GameOutcome): The desired game outcome.

        Returns:
            Gesture: The gesture required to achieve the desired
                game_outcome.
        """
        if game_outcome == GameOutcome.DRAW:
            return input_gesture
        elif game_outcome == GameOutcome.LOSE:
            return BEATS_MAPPING[input_gesture]
        else:
            return {v: k for k, v in BEATS_MAPPING.items()}[input_gesture]

    @property
    def score(self) -> int:
        """The total score for this game, for the player (response
        gesture).

        Returns:
            int: The score related to the gesture.
        """
        return self.response_gesture.value + self.game_outcome.value


def part_one(input_lines: list[str]) -> int:
    """Part one assumes the second value in the game input is the
    response gesture.

    Args:
        input_lines (list[str]): List of games.

    Returns:
        int: The total score for the player.
    """
    total: int = 0
    for line in input_lines:
        input_move, response_move = line.split(" ")
        game = Game(
            input_gesture=INPUT_MAPPING[input_move],
            response_gesture=INPUT_MAPPING[response_move],
        )
        total += game.score
    return total


def part_two(input_lines: list[str]) -> int:
    """Part two assumes the second value in the game input is the
    desired outcome of the game.

    Args:
        input_lines (list[str]): List of games.

    Returns:
        int: The total score for the player.
    """
    total: int = 0
    for line in input_lines:
        input_move, response_move = line.split(" ")
        game = Game(
            input_gesture=INPUT_MAPPING[input_move],
            game_outcome=OUTCOME_MAPPING[response_move],
        )
        total += game.score
    return total


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_2.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    score = part_one(input_lines)
    print("Part one:", score)

    # Determine the output for part two
    score = part_two(input_lines)
    print("Part two:", score)
