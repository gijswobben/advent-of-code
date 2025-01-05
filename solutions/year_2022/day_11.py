# https://adventofcode.com/2022/day/11

from __future__ import annotations

import functools
from pathlib import Path
from typing import Callable


class Monkey:
    """Represents a single monkey in a group.

    Args:
        name (str): Name of this monkey.
        starting_items (list[int]): The items that this monkey initially
            has.
        operation (Callable[[int], int]): The operation that this monkey
            performs on the items.
        test_method (Callable[[int], str]): The function this monkey
            uses to decide where to throw the item.
        test_divisble_by (int): The "divisible by" value used in the
            test_method.
    """

    def __init__(
        self,
        name: str,
        starting_items: list[int],
        operation: Callable[[int], int],
        test_method: Callable[[int], str],
        test_divisble_by: int,
    ) -> None:
        self.name = name
        self.items: list[int] = starting_items
        self.operation = operation
        self.test_method = test_method
        self.group: MonkeyGroup | None = None
        self.n_items_inspected = 0
        self.test_divisble_by = test_divisble_by

    def take_turn(self, reduce_worry_level: bool = True):
        """Let this monkey take a turn.

        Args:
            reduce_worry_level (bool, optional): Whether or not the
                worry level should be reduced. Defaults to True.

        Raises:
            Exception: Raised if this monkey is not part of a group.
        """

        # Stop if this monkey is not part of a group
        if self.group is None:
            raise Exception(f"{self.name} not in a group!")

        # Inspect all items in posession
        self.n_items_inspected += len(self.items)
        self.items = [self.operation(item) for item in self.items]

        # Item is not broken, worry level is reduced
        if reduce_worry_level:
            self.items = [item // 3 for item in self.items]
        else:
            # Combine the "divisible_by" properties to get the largest
            # value that should still be left after reduction
            modulo = functools.reduce(
                lambda a, b: a * b,
                [monkey.test_divisble_by for monkey in self.group.monkeys.values()],
            )
            self.items = [item % modulo for item in self.items]

        # Throw all items to other monkeys in the group
        for item in self.items:
            throw_to = self.test_method(item)
            self.group.monkeys[throw_to].catch(item)

        # This monkey no longer has any items
        self.items = []

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Monkey:
        """Create a new monkey from lines of text.

        Args:
            input_lines (list[str]): The text that defines the monkey.

        Returns:
            Monkey: The resulting Monkey object.
        """

        # Name is on the first line
        name = input_lines[0].strip(":")

        # The starting items are comma separated on the second line
        starting_items = [
            int(item.strip()) for item in input_lines[1].split(": ")[1].split(",")
        ]

        # Create a lambda function from the third line
        operation = eval(f"lambda old: {input_lines[2].split('new = ')[1]}")

        # Remaining lines contain information about the test method
        test_divisble_by = int(input_lines[3].split("divisible by ")[1])
        if_true = input_lines[4].split("throw to ")[1].capitalize()
        if_false = input_lines[5].split("throw to ")[1].capitalize()

        def _test_method(worry_level: int) -> str:
            return if_true if worry_level % test_divisble_by == 0 else if_false

        return Monkey(
            name=name,
            starting_items=starting_items,
            operation=operation,
            test_method=_test_method,
            test_divisble_by=test_divisble_by,
        )

    def catch(self, item: int):
        """This monkey catches an item and adds it to its list of items.

        Args:
            item (int): The item the monkey should catch.
        """
        self.items.append(item)

    def __repr__(self) -> str:
        return f"{self.name}: {', '.join([str(item) for item in self.items])}"


class MonkeyGroup:
    """Represents a group of monkeys.

    Args:
        monkeys (list[Monkey]): List of monkeys that are part of this
            group.
        reduce_worry_level (bool): Whether or not the worry level is
            divided by 3 (for part one). Defaults to True.
    """

    def __init__(self, monkeys: list[Monkey], reduce_worry_level: bool = True) -> None:
        self.reduce_worry_level = reduce_worry_level
        self.monkeys: dict[str, Monkey] = {monkey.name: monkey for monkey in monkeys}
        for monkey in self.monkeys.values():
            monkey.group = self

    def round(self):
        """Run a full round by giving all monkeys in the group a turn."""
        for monkey in self.monkeys.values():
            monkey.take_turn(reduce_worry_level=self.reduce_worry_level)


def part_one(input_lines: list[str]) -> int:

    # Create monkeys from the instructions
    monkey_definitions: list[list[str]] = []
    buffer: list[str] = []
    for line in input_lines:
        if line == "":
            monkey_definitions.append(buffer)
            buffer = []
        else:
            buffer.append(line)
    monkey_definitions.append(buffer)

    # Put all monkeys in a group
    group = MonkeyGroup(
        monkeys=[Monkey.from_text(definition) for definition in monkey_definitions]
    )

    # Run for a number of rounds
    for _ in range(20):
        group.round()

    # Get the top 2 most active monkeys in the group
    top_2_items_inspected = sorted(
        [monkey.n_items_inspected for monkey in group.monkeys.values()], reverse=True
    )[:2]

    # Multiply top 2 monkeys for the "monkey business" score
    return top_2_items_inspected[0] * top_2_items_inspected[1]


def part_two(input_lines: list[str]) -> int:

    # Create monkeys from the instructions
    monkey_definitions: list[list[str]] = []
    buffer: list[str] = []
    for line in input_lines:
        if line == "":
            monkey_definitions.append(buffer)
            buffer = []
        else:
            buffer.append(line)
    monkey_definitions.append(buffer)

    # Put all monkeys in a group
    group = MonkeyGroup(
        monkeys=[Monkey.from_text(definition) for definition in monkey_definitions],
        reduce_worry_level=False,
    )

    # Run for a number of rounds
    for _ in range(10000):
        group.round()

    # Get the top 2 most active monkeys in the group
    top_2_items_inspected = sorted(
        [monkey.n_items_inspected for monkey in group.monkeys.values()], reverse=True
    )[:2]

    # Multiply top 2 monkeys for the "monkey business" score
    return top_2_items_inspected[0] * top_2_items_inspected[1]


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_11.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
