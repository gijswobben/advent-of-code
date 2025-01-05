"""Assignment for day 2 of 2024 Advent of Code.

https://adventofcode.com/2024/day/2
"""

from pathlib import Path


class Report:
    """Representation of a single report (line).

    Args:
    ----
        line (str): The line of the report.
        tolerance (tuple[int, int], optional): The tolerance for the
            sequence. Defaults to (1, 3).
        has_problem_dampener (bool, optional): Whether the report has a
            problem dampener. Defaults to False.

    """

    def __init__(
        self,
        line: str,
        tolerance: tuple[int, int] = (1, 3),
        has_problem_dampener: bool = False,
    ):
        self.numbers = list(map(int, line.split()))
        self.tolerance = tolerance
        self.has_problem_dampener = has_problem_dampener

    def _all_increasing(self, numbers: list[int]) -> bool:
        return all(numbers[i] < numbers[i + 1] for i in range(len(numbers) - 1))

    def _all_decreasing(self, numbers: list[int]) -> bool:
        return all(numbers[i] > numbers[i + 1] for i in range(len(numbers) - 1))

    def _all_within_max_tolerance(self, numbers: list[int]) -> bool:
        return all(
            difference >= self.tolerance[0] and difference <= self.tolerance[1]
            for difference in [
                abs(numbers[i] - numbers[i + 1]) for i in range(len(numbers) - 1)
            ]
        )

    def _test_safe(self, numbers: list[int]) -> bool:
        return (
            self._all_increasing(numbers) or self._all_decreasing(numbers)
        ) and self._all_within_max_tolerance(numbers)

    @property
    def is_safe(self) -> bool:
        """Check if the report is safe."""
        # Check the full sequence
        if self._test_safe(self.numbers):
            return True

        # If there is a report dampener, check all possible sequences
        # with one number removed
        if self.has_problem_dampener:
            for i in range(len(self.numbers)):
                # Make a copy and remove the number at the index
                numbers = [
                    number for index, number in enumerate(self.numbers) if index != i
                ]
                # Check if the sequence is safe
                if self._test_safe(numbers):
                    return True

        # The sequence is not safe by any means
        return False


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    reports = [Report(input_line) for input_line in input_lines]
    return sum(report.is_safe for report in reports)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    reports = [
        Report(input_line, has_problem_dampener=True) for input_line in input_lines
    ]
    return sum(report.is_safe for report in reports)


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data/day_2.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
