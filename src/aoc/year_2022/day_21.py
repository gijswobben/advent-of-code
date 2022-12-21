# https://adventofcode.com/2022/day/21

import math
import re
from pathlib import Path

from scipy.optimize import OptimizeResult, minimize_scalar

FUNCTION_PATTERN = re.compile(r"(?P<left>\w+\s)(?P<operator>.)(?P<right>\s\w+)")


class Monkey:
    """Represents a single monkey in the group.

    Monkeys yell either a static value, or the result of some kind of
    function.

    Args:
        name (str): Name of this monkey.
        function (int | str): The static value this monkey yells as a
            int, or the function as a strings.
    """

    def __init__(self, name: str, function: str) -> None:
        self.name = name

        # Check if the function is a number
        self.function: int | str
        try:
            self.function = int(function)
        except ValueError:
            match = re.search(FUNCTION_PATTERN, function)
            if match is None:
                raise Exception("Invalid function")
            self._left = match.group("left").strip()
            self._right = match.group("right").strip()
            self.function = function

    def yell(self, known: dict[str, int]) -> int | None:
        """Ask the monkey to yell its value or result of the function.

        Args:
            known (dict[str, int]): The values that the other monkeys
                yelled already.

        Returns:
            int | None: The result or None if the input values are not
                known yet.
        """
        if isinstance(self.function, int):
            return self.function
        else:
            try:
                return int(eval(self.function, {}, known))
            except Exception:
                return None


class Root(Monkey):
    """Special monkey that doesn't yell a number, but the difference
    between 2 numbers. The goal is to set numbers in such a way that
    this monkey yells 0.

    Args:
        name (str): Name of this monkey. function (int | str): The
        static value this monkey yells as a
            int, or the function as a strings.
    """

    def __init__(self, name: str, function: str) -> None:
        super(Root, self).__init__(name, function)

        # Overwrite the function property by replacing the operator with
        # `-` so it returns the difference between left and right. The
        # goal is to find a number that satisfies left - right = 0
        self.function: str = re.sub(
            FUNCTION_PATTERN,
            r"\g<left>-\g<right>",
            self.function,
        )


class Simulator:
    """A simulator that can be used to "solve" the riddle.

    The simulator can simulate what happens for a particular value that
    the human yells. Such simulations return the difference between left
    and right for the root monkey. The solution is found when the root
    monkey yells 0 (no difference).

    Args:
        monkeys (list[Monkey]): The monkeys that are playing the riddle.
    """

    def __init__(self, monkeys: list[Monkey]) -> None:
        self.monkeys = monkeys

    def simulate(self, X) -> int:
        """Simulate what happens when the "human" yells a particular number (X).

        Args:
            X (int): Number the human yells.

        Returns:
            int: The response from the root monkey.
        """
        known: dict[str, int] = {
            "humn": X,
            **{
                monkey.name: monkey.function
                for monkey in self.monkeys
                if isinstance(monkey.function, int)
            },
        }
        function_monkeys = [
            monkey for monkey in self.monkeys if not isinstance(monkey.function, int)
        ]
        while True:
            for monkey in function_monkeys:
                if isinstance(monkey, Root):
                    loss = monkey.yell(known=known)
                    if loss is None:
                        pass
                    else:
                        return loss

                else:
                    new_value = monkey.yell(known=known)
                    if new_value is not None:
                        known[monkey.name] = new_value

    def find_solution(self) -> int:
        """Find the solution (value the human should yell).

        Returns:
            int: The value as an integer.
        """

        # simulate(X) returns the result of the root monkey. This value
        # should be 0 to find the solution; minimize the function
        # `abs(simulate(X))`.
        result: OptimizeResult = minimize_scalar(
            lambda X: abs(self.simulate(X)),
            tol=1e-24,  # Low tolerance is needed to find the solution
        )

        # If the exact solution was found, return it as an integer
        if result.success:
            return int(round(result.x))

        # Try the surrounding numbers if no exact solution was found
        else:
            for i in range(math.floor(result.x) - 10, math.floor(result.x) + 10):
                if self.simulate(i) == 0:
                    return i
        return int(round(result.x))


def part_one(input_lines: list[str]) -> int:

    # Create all the monkeys from the input
    monkeys = [Monkey(*line.split(": ")) for line in input_lines]

    # Keep track of all known values yelled by the monkeys
    known: dict[str, int] = {}

    # Keep yelling until the root monkey has yelled its value
    while "root" not in known:
        for monkey in monkeys:
            new_value = monkey.yell(known=known)
            if new_value is not None:
                known[monkey.name] = new_value

    return int(known["root"])


def part_two(input_lines: list[str]) -> int:

    # Create all the monkeys from the input; create a "special" monkey
    # for the root monkey
    monkeys = [
        Root(*line.split(": "))
        if line.startswith("root")
        else Monkey(*line.split(": "))
        for line in input_lines
        if not line.startswith("humn")
    ]

    # Create a simulator for the monkeys
    model = Simulator(monkeys=monkeys)

    # Find the value for the human by minimizing the simulation
    return model.find_solution()


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_21.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
