"""Assignment for day 7 of 2024 Advent of Code.

https://adventofcode.com/2024/day/7
"""

import itertools
import operator
from functools import cached_property
from pathlib import Path
from typing import Callable

# Operators used in part 1
operators_1: dict[str, Callable[[int, int], int]] = {
    "ADD": operator.add,
    "MUL": operator.mul,
}

# Operators used in part 2
operators_2: dict[str, Callable[[int, int], int]] = {
    "ADD": operator.add,
    "MUL": operator.mul,
    "CONCAT": lambda x, y: int(str(x) + str(y)),
}


class Equation:
    """Class to represent an equation.

    Args:
    ----
        outcome: The expected outcome.
        values: The values to use in the equation.
        operators: The operators to use.

    """

    def __init__(
        self,
        outcome: int,
        values: list[int],
        operators: dict[str, Callable[[int, int], int]],
    ) -> None:
        self.outcome = outcome
        self.values = values
        self.operators = operators

    def evaluate(self, selected_operators: tuple[str, ...]) -> int:
        """Evaluate the equation, left to right.

        Args:
        ----
            selected_operators: The operators to use.

        Returns:
        -------
            The result of the equation.

        """
        # Start with the value of the first number
        result = self.values[0]

        # Loop all values and apply the operators, one by one
        for i, value in enumerate(self.values[1:]):
            result = self.operators[selected_operators[i]](result, value)

            # If the result is already higher than the expected outcome,
            # we can stop the calculation
            if result > self.outcome:
                break
        return result

    def find_operators(self) -> list[Callable[[int, int], int]]:
        """Find the operators for the equation.

        Returns
        -------
        The operators for the equation.

        """
        # Determine the number of positions to fill with operators
        positions = len(self.values) - 1

        # Loop all possible combinations of operators and check if the
        # outcome is the same as the expected outcome. If so, add the
        # operators to the list of valid operators
        valid_operators = []
        for option in itertools.product(self.operators.keys(), repeat=positions):
            if self.evaluate(option) == self.outcome:
                valid_operators.append(option)

        return valid_operators

    @cached_property
    def is_valid(self) -> bool:
        """Check if the equation is valid (has a solution)."""
        return len(self.find_operators()) > 0


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    # Parse the input lines into equations
    equations = []
    for line in input_lines:
        outcome, values = line.split(":")
        equations.append(
            Equation(
                outcome=int(outcome),
                values=list(map(int, values.split())),
                operators=operators_1,
            ),
        )

    # Return the sum of the outcomes of the valid equations
    return sum([equation.outcome for equation in equations if equation.is_valid])


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    # Parse the input lines into equations
    equations = []
    for line in input_lines:
        outcome, values = line.split(":")
        equations.append(
            Equation(
                outcome=int(outcome),
                values=list(map(int, values.split())),
                operators=operators_2,
            ),
        )

    # Return the sum of the outcomes of the valid equations
    return sum([equation.outcome for equation in equations if equation.is_valid])


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_7.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
