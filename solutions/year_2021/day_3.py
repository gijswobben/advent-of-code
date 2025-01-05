# https://adventofcode.com/2021/day/3

from pathlib import Path
from typing import Literal


class DiagnosticsReport:
    def __init__(self, report: list[str]) -> None:
        self.report = report

    @property
    def gamma_rate(self) -> int:
        # Convert the binary strings to decimal numbers
        return int(self.gamma_rate_binary, 2)

    @property
    def gamma_rate_binary(self) -> str:
        gamma_rate_bin = ""

        # Loop the digits from left to right
        for index in range(len(self.report[0])):

            # Keep track of the number of digits
            zeroes = sum([1 if line[index] == "0" else 0 for line in self.report])
            ones = sum([1 if line[index] == "1" else 0 for line in self.report])

            # Add the next character to the binary string
            gamma_rate_bin += "0" if zeroes > ones else "1"

        return gamma_rate_bin

    @property
    def epsilon_rate_binary(self) -> str:
        return "".join(
            ["1" if character == "0" else "0" for character in self.gamma_rate_binary]
        )

    @property
    def epsilon_rate(self) -> int:
        return int(self.epsilon_rate_binary, 2)

    @property
    def energy_consumption(self) -> int:
        return self.gamma_rate * self.epsilon_rate

    def most_common_bit(
        self, report: list[str], index: int, tie: Literal["1", "0"]
    ) -> Literal["1", "0"]:
        zeroes = sum([1 if line[index] == "0" else 0 for line in report])
        ones = sum([1 if line[index] == "1" else 0 for line in report])
        if zeroes == ones:
            return tie
        elif zeroes > ones:
            return "0"
        else:
            return "1"

    def least_common_bit(
        self, report: list[str], index: int, tie: Literal["1", "0"]
    ) -> Literal["1", "0"]:
        zeroes = sum([1 if line[index] == "0" else 0 for line in report])
        ones = sum([1 if line[index] == "1" else 0 for line in report])
        if zeroes == ones:
            return tie
        elif zeroes < ones:
            return "0"
        else:
            return "1"

    @property
    def oxygen_generator_rating(self) -> int:

        # Make a copy of the full report
        filtered_report = self.report.copy()

        position = 0
        while len(filtered_report) > 1 and position < len(self.report[0]):

            # Determine the most common bits in the remaining report
            most_common_bit = self.most_common_bit(
                filtered_report, index=position, tie="1"
            )

            # Filter the report to only those numbers that have the most
            # common bit at the correct position
            filtered_report = [
                line for line in filtered_report if line[position] == most_common_bit
            ]

            position += 1

        return int(filtered_report[0], 2)

    @property
    def co2_scrubber_rating(self) -> int:

        # Make a copy of the full report
        filtered_report = self.report.copy()

        position = 0
        while len(filtered_report) > 1 and position < len(self.report[0]):

            # Determine the most common bits in the remaining report
            least_common_bit = self.least_common_bit(
                filtered_report, index=position, tie="0"
            )

            # Filter the report to only those numbers that have the most
            # common bit at the correct position
            filtered_report = [
                line for line in filtered_report if line[position] == least_common_bit
            ]

            position += 1

        return int(filtered_report[0], 2)


def part_one(input_lines: list[str]) -> int:
    report = DiagnosticsReport(input_lines)
    return report.energy_consumption


def part_two(input_lines: list[str]) -> int:
    report = DiagnosticsReport(input_lines)
    return report.oxygen_generator_rating * report.co2_scrubber_rating


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_3.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
