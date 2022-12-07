# https://adventofcode.com/2022/day/5

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

MOVE_PATTERN = re.compile(r"move (?P<quantity>\d+) from (?P<from>\d+) to (?P<to>\d+)")


class Crate:
    """Class that represents an individual crate.

    Args:
        description (str): The description written on the crate.
    """

    def __init__(self, description: str):
        self.description = description

    def __repr__(self) -> str:
        return f"[{self.description}]"


class Stack:
    """Class that represents a stack of crates."""

    def __init__(self) -> None:
        self.contents: list[Crate] = []

    def add(self, item: Crate):
        """Add a new crate to this stack.

        Args:
            item (Crate): The crate to add.
        """
        self.contents.append(item)

    def remove(self) -> Crate | None:
        """Remove a crate from this stack if the stack is not empty.

        Returns:
            Crate | None: The removed crate, if the stack was not empty.
        """
        if len(self.contents) == 0:
            return None
        return self.contents.pop(-1)

    @property
    def top_item(self) -> Crate | None:
        """Return to top item on this stack without removing it.

        Returns:
            Crate | None: The top crate if the stack was not empty.
        """
        if len(self.contents) == 0:
            return None
        return self.contents[-1]

    def __repr__(self) -> str:
        return f"Stack{[crate.description for crate in self.contents]!r}"


@dataclass
class Move:
    """Container for holding information about a move of crates."""

    quantity: int
    from_stack: int
    to_stack: int

    @classmethod
    def from_string(self, input_string: str) -> Move:
        """Parse a string into a move object.

        The move object holds information about the number of crates
        that should be moved, and the source and destination stacks.

        Args:
            input_string (str): The move information as a string.

        Raises:
            Exception: Raised when an invalid move was parsed.

        Returns:
            Move: The move information.
        """
        match = re.match(MOVE_PATTERN, input_string)
        if match is not None:
            quantity = int(match.group("quantity"))
            from_stack = int(match.group("from"))
            to_stack = int(match.group("to"))
            return Move(quantity=quantity, from_stack=from_stack, to_stack=to_stack)
        else:
            raise Exception("Invalid move")


class Crane:
    """Base class for the different types of cranes.

    Args:
        ship (Ship): The ship that this crane operates on.
    """

    def __init__(self, ship: Ship) -> None:
        self.ship = ship


class CrateMover9000(Crane):
    """Type of crane that moves one crate at a time."""

    def move(self, move: Move):
        """Use this crane to move crates from one stack to another.

        Args:
            move (Move): The information about the move.
        """
        for _ in range(move.quantity):
            crate = self.ship.stacks[move.from_stack].remove()
            if crate is not None:
                self.ship.stacks[move.to_stack].add(crate)


class CrateMover9001(Crane):
    """Type of crane that moves multiple crate at a time."""

    def move(self, move: Move):
        """Use this crane to move crates from one stack to another.

        Args:
            move (Move): The information about the move.
        """
        crates: list[Crate] = []
        for _ in range(move.quantity):
            crate = self.ship.stacks[move.from_stack].remove()
            if crate is not None:
                crates.insert(0, crate)
        for crate in crates:
            self.ship.stacks[move.to_stack].add(crate)


class Ship:
    """Class that represents a ship with stacks of crates.

    Args:
        stacks (dict[int, Stack]): A mapping between stack number
            (starting from 1) and the corresponding stack of crates.
    """

    def __init__(self, stacks: dict[int, Stack]) -> None:
        self.stacks = stacks

    @property
    def top_items(self) -> list[Crate | None]:
        """A list of the top item for each stack on this ship.

        Returns:
            list[Crate | None]: List of crates or None if a stack is
                empty.
        """
        return [stack.top_item for stack in self.stacks.values()]

    @classmethod
    def from_text(cls, state: list[str]) -> Ship:
        """Create a ship from a list of strings.

        The `state` argument should be a list of strings where each
        string contains information about crates in stacks (see test
        input).

        Args:
            state (list[str]): List of lines of crate information.

        Returns:
            Ship: The ship with stacks of crates.
        """
        stacks: dict[int, Stack] = {}
        for line in reversed(state[:-1]):
            for index in range(len(line) // 3):
                if index + 1 not in stacks:
                    stacks[index + 1] = Stack()
                crate_description = (
                    line[index * 3 + index : index * 3 + index + 3]
                    .strip(" ")
                    .strip("[")
                    .strip("]")
                )
                if crate_description != "":
                    stacks[index + 1].add(Crate(description=crate_description))
        return Ship(stacks=stacks)

    def __repr__(self) -> str:
        output: list[str] = []
        max_items = max([len(stack.contents) for stack in self.stacks.values()])
        for line_index in reversed(range(max_items)):
            line = ""
            for stack in self.stacks.values():
                if len(stack.contents) - 1 < line_index:
                    line += "   "
                else:
                    line += f"{stack.contents[line_index]!r}"
                line += " "
            output.append(line)
        output.append(
            " ".join([f" {stack_number} " for stack_number in self.stacks.keys()])
        )
        return "\n".join(output)


def part_one(input_lines: list[str]) -> str:

    # Determine where the state ends and the moves begin
    for index, line in enumerate(input_lines):
        if line.startswith("move "):
            state = input_lines[: index - 1]
            moves = input_lines[index:]
            break

    # Create a ship
    ship = Ship.from_text(state=state)

    # Create a crane for this ship
    crane = CrateMover9000(ship=ship)

    # Use the crane to execute a list of moves
    for line in moves:
        crane.move(Move.from_string(line))

    # Combine the descriptions of the top crates in each stack
    return "".join([crate.description for crate in ship.top_items if crate is not None])


def part_two(input_lines: list[str]) -> str:

    # Determine where the state ends and the moves begin
    for index, line in enumerate(input_lines):
        if line.startswith("move "):
            state = input_lines[: index - 1]
            moves = input_lines[index:]
            break

    # Create a ship
    ship = Ship.from_text(state=state)

    # Create a crane for this ship
    crane = CrateMover9001(ship=ship)

    # Use the crane to execute a list of moves
    for line in moves:
        crane.move(Move.from_string(line))

    # Combine the descriptions of the top crates in each stack
    return "".join([crate.description for crate in ship.top_items if crate is not None])


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_5.txt", "r") as f:
        input_lines = [line.rstrip("\n") for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
