# https://adventofcode.com/2021/day/14

import itertools
from collections import defaultdict
from pathlib import Path


class PolymerTemplate:
    """Represents a polymer template.

    Args:
        template (str): The initials template of the polymer.
        rules (dict[tuple[str, str], str]): A set of rules. If the tuple
            (left, right) is encountered in the polymer, a new value is
            inserted in between
    """

    def __init__(self, template: str, rules: dict[tuple[str, str], str]) -> None:
        self.template = template
        self.rules = rules

        # Keep track of the number of pairs
        self._pairs: dict[tuple[str, str], int] = defaultdict(int)
        for left, right in itertools.pairwise(template):
            self._pairs[(left, right)] += 1

    def step(self) -> None:
        """Simulate 1 step of insertations."""

        # Keep track of the updates during this step, don't apply them
        # directly to avoid changing the counts
        updates: dict[tuple[str, str], int] = defaultdict(int)

        # Go over all the rules
        for (left, right), insertation in self.rules.items():

            # The number of matching pairs that will be split by the
            # insertation
            n_matches = self._pairs[(left, right)]

            # After insertation there are 2 new pairs, both occur as
            # frequent as the original pair
            updates[(left, insertation)] += n_matches
            updates[(insertation, right)] += n_matches

            # The original pair no longer exists (it's now split)
            updates[(left, right)] -= n_matches

        # At the end of the step, apply all the updates at once
        for (left, right), change in updates.items():
            self._pairs[(left, right)] += change

    @property
    def most_common(self) -> int:
        counts: dict[str, int] = defaultdict(int)
        for (_, right), number in self._pairs.items():
            counts[right] += number
        return sorted(counts.values())[-1]

    @property
    def least_common(self) -> int:
        counts: dict[str, int] = defaultdict(int)
        for (_, right), number in self._pairs.items():
            counts[right] += number
        return sorted(counts.values())[0]


def parse_rule(string: str) -> tuple[tuple[str, str], str]:
    left, right = string.split(" -> ")
    return ((left[0], left[1]), right)


def part_one(input_lines: list[str]) -> int:

    # Parse the rules (skip the first 2 lines)
    rules: dict[tuple[str, str], str] = {
        key: value for key, value in [parse_rule(line) for line in input_lines[2:]]
    }

    # Create the template from the first line and the parsed rules
    template = PolymerTemplate(template=input_lines[0], rules=rules)

    # Iterate N steps and calculate the output
    for _ in range(10):
        template.step()
    return template.most_common - template.least_common


def part_two(input_lines: list[str]) -> int:

    # Parse the rules (skip the first 2 lines)
    rules: dict[tuple[str, str], str] = {
        key: value for key, value in [parse_rule(line) for line in input_lines[2:]]
    }

    # Create the template from the first line and the parsed rules
    template = PolymerTemplate(template=input_lines[0], rules=rules)

    # Iterate N steps and calculate the output
    for _ in range(40):
        template.step()
    return template.most_common - template.least_common


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_14.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
