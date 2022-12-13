# https://adventofcode.com/2022/day/13

from __future__ import annotations

from pathlib import Path
from typing import Any, Union

RecursiveListType = list[int | Union[int, "RecursiveListType"]]


class Packet:
    """Class that represents a single packet.

    Packets contain data and can be compared based on their data (full
    set of compare rules in the challenge description).

    Args:
        data (RecursiveListType): List of integers or list of integers
            recursive.
    """

    def __init__(self, data: RecursiveListType) -> None:
        self.data = data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.data!r}>"

    def __lt__(self, other: Packet | Any) -> bool:
        """Magic method that is used when Packets are compared using the
        `<` operator.

        Checks if this Packet is "lower than" another Packet.

        Args:
            other (Packet | Any): The Packet to compare against.

        Raises:
            Exception: Raised when the other argument is not a Packet or
                when it is not possible to determine which Packet was
                "larger".

        Returns:
            bool: True when this Packet was "lower" than the other.
        """
        if not isinstance(other, Packet):
            raise Exception(f"Invalid compare between Packet and {type(other)}")

        output = self._compare_lists(self.data, other.data)
        if output is None:
            raise Exception("Packets are identical, cannot determine order")
        return output

    def _compare_lists(
        self, left: RecursiveListType, right: RecursiveListType
    ) -> bool | None:
        """Helper method to compare 2 lists according to a set of rules.

        Args:
            left (RecursiveListType): The left list (possibly nested).
            right (RecursiveListType): The right list (possibly nested).

        Returns:
            bool | None: A boolean value when it was possible to
                determine which list was "larger" (True means left is
                larger, False means right is larger) or None if it was
                not possible to determine which list was "larger".
        """

        # Go over all items in pairs
        for index in range(max(len(left), len(right))):

            # Left runs out
            if index >= len(left):
                return True
            # Right runs out
            elif index >= len(right):
                return False

            # Get the items at the position of the index
            left_item = left[index]
            right_item = right[index]

            # If exactly one value is an integer
            if isinstance(left_item, int) and isinstance(right_item, list):
                left_item = [left_item]
            elif isinstance(left_item, list) and isinstance(right_item, int):
                right_item = [right_item]

            # If both are integers
            if isinstance(left_item, int) and isinstance(right_item, int):
                if left_item < right_item:
                    return True
                elif left_item > right_item:
                    return False

            # If both values are lists
            if isinstance(left_item, list) and isinstance(right_item, list):
                sub_compare = self._compare_lists(left_item, right_item)
                if sub_compare is not None:
                    return sub_compare

        # If there was no deciding factor
        return None


def part_one(input_lines: list[str]) -> int:

    # Loop all sets of 3 lines
    total = 0
    for index in range(len(input_lines) // 3 + 1):

        # Extract left and right
        left = Packet(data=eval(input_lines[index * 3], {}, {}))
        right = Packet(data=eval(input_lines[index * 3 + 1], {}, {}))

        # If left is smaller than right, they are in the right order
        if left < right:
            total += index + 1

    return total


def part_two(input_lines: list[str]) -> int:

    # Add the dividers to the initial list
    divider_one = Packet(data=[[2]])
    divider_two = Packet(data=[[6]])
    packets: list[Packet] = [divider_one, divider_two]

    # Add the rest of the packets
    for line in input_lines:
        if line == "":
            continue
        packets.append(Packet(data=eval(line, {}, {})))

    # Sort the packets (uses the __lt__ method of the packet by default)
    packets.sort()

    # Get the indices of the dividers
    position_divider_one = packets.index(divider_one) + 1
    position_divider_two = packets.index(divider_two) + 1

    # Multiply the indices of the dividers to get the answer
    return position_divider_one * position_divider_two


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_13.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
