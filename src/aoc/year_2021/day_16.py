# https://adventofcode.com/2021/day/16

from __future__ import annotations

import functools
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable


def parse_packet(binary: str) -> Packet:
    """Parse a packet and subpackets from a binary string.

    Args:
        binary (str): The binary value as a string.

    Returns:
        Packet: The parsed packet and subpackets.
    """

    # Read the packet version and type ID
    packet_version = int(binary[:3], 2)
    type_id = int(binary[3:6], 2)

    # Create either a Literal or Operator packet
    packet = (
        LiteralPacket(version=packet_version, binary=binary)
        if type_id == 4
        else OperatorPacket(version=packet_version, type_id=type_id, binary=binary)
    )

    return packet


class Packet(ABC):
    """Base class for all packet types.

    Args:
        version (int): The packet version number.
        binary (str): The binary content of this packet (and
            subpackets).
    """

    end_bit: int

    def __init__(self, version: int, binary: str) -> None:
        self.version = version
        self.binary = binary

    @property
    @abstractmethod
    def total_value(self) -> int:
        ...


class OperatorPacket(Packet):
    """Packet that performs some kind of operation on its subpackets."""

    def __init__(self, version: int, type_id: int, binary: str) -> None:
        super().__init__(version, binary)
        self.subpackets: list[Packet] = []

        # Store the type ID, used to determine the kind of operation
        self.type_id = type_id

        # 6th bit contains the type of lenght indication
        self.length_type_id = int(self.binary[6])

        if self.length_type_id == 0:

            # Determine how many bits need to be read (unknown number of
            # packets)
            subpacket_length = int(self.binary[7:22], 2)
            self.end_bit = (
                22 + subpacket_length
            )  # We now know how large this packet is in total

            # Keep reading the remainder until we've reached the desired
            # length
            remainder = self.binary[22:]
            while subpacket_length > 0:

                # Read the next subpacket
                subpacket = parse_packet(binary=remainder)
                self.subpackets.append(subpacket)

                # Use the end mark of the subpacket to determine how
                # much to still read
                subpacket_length -= subpacket.end_bit
                remainder = remainder[subpacket.end_bit :]

        else:

            # Determine the number of subpackets to read
            n_subpackets = int(self.binary[7:18], 2)
            self.end_bit = 18

            # Read the desired number of subpackets
            remainder = self.binary[18:]
            for _ in range(n_subpackets):

                # Read the next subpacket
                subpacket = parse_packet(binary=remainder)
                self.subpackets.append(subpacket)

                # Don't read the same bit twice
                remainder = remainder[subpacket.end_bit :]
                self.end_bit += subpacket.end_bit

    @property
    def total_value(self) -> int:

        # Create a mapping between the type ID and the operation to
        # perform on the subpackets
        type_mapping: dict[int, Callable[[list[int]], int]] = {
            0: sum,
            1: lambda subpackets: functools.reduce(lambda a, b: a * b, subpackets),
            2: min,
            3: max,
            5: lambda subpackets: 1 if subpackets[0] > subpackets[1] else 0,
            6: lambda subpackets: 1 if subpackets[0] < subpackets[1] else 0,
            7: lambda subpackets: 1 if subpackets[0] == subpackets[1] else 0,
        }

        # Apply the function to the values of the subpackets
        return type_mapping[self.type_id](
            [subpacket.total_value for subpacket in self.subpackets]
        )

    def __repr__(self) -> str:
        return f"OperatorPacket(version={self.version})"


class LiteralPacket(Packet):
    """Represents a packet that contains a literal value."""

    def __init__(self, version: int, binary: str) -> None:
        super(LiteralPacket, self).__init__(version, binary)

        # For literal values, convert to decimal
        self.end_bit = 0
        number = ""

        # Loop the rest of the binary (excluding header) in groups of 5
        # bits
        for index, group in enumerate(
            [
                self.binary[6:][i * 5 : 5 * i + 5]
                for i in range(len(self.binary[6:]) // 5)
            ]
        ):

            # Add the last 4 bits to the number
            number += group[1:]

            # Stop if this group starts with a "0" bit
            if group[0] == "0":
                self.end_bit = 6 + 5 * index + 5
                break

        # Convert binary number to decimal
        self.value = int(number, 2)

    @property
    def total_value(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"LiteralPacket(version={self.version}, value={self.value})"


def part_one(input_lines: list[str]) -> int:

    # Parse the Hex number to binary and parse the packet
    binary = "".join([f"{int(character, 16):04b}" for character in input_lines[0]])
    packet = parse_packet(binary)

    def _recursive_sum_version_numbers(packet: Packet) -> int:
        total = packet.version

        if isinstance(packet, OperatorPacket):
            for subpacket in packet.subpackets:
                total += _recursive_sum_version_numbers(subpacket)

        return total

    # Recurse this packet and all its subpackets and sum the version
    # numbers
    return _recursive_sum_version_numbers(packet)


def part_two(input_lines: list[str]) -> int:

    # Parse the Hex number to binary and parse the packet
    binary = "".join([f"{int(character, 16):04b}" for character in input_lines[0]])
    packet = parse_packet(binary)

    # Return the total value
    return packet.total_value


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_16.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
