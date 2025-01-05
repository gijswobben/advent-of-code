"""Assignment for day 5 of 2024 Advent of Code.

https://adventofcode.com/2024/day/5
"""

from pathlib import Path

from pydantic import BaseModel


class Rule(BaseModel):
    left: int
    right: int

    def check(self, page_numbers: list[int]) -> bool:
        if self.left not in page_numbers or self.right not in page_numbers:
            return True
        return page_numbers.index(self.left) < page_numbers.index(self.right)


class Update:
    def __init__(self, page_numbers: list[int], rules: list[Rule]) -> None:
        self.page_numbers = page_numbers
        self.rules = rules

    def fix_order(self) -> None:
        # Find out which rules apply to this update
        applicable_rules = [
            rule
            for rule in self.rules
            if rule.left in self.page_numbers and rule.right in self.page_numbers
        ]

        # If the page_numbers are already in the correct order, return
        if all(rule.check(self.page_numbers) for rule in applicable_rules):
            return

        while not all(rule.check(self.page_numbers) for rule in applicable_rules):
            for rule in applicable_rules:
                if not rule.check(self.page_numbers):
                    # Find the index of the left and right page_numbers
                    left_index = self.page_numbers.index(rule.left)
                    right_index = self.page_numbers.index(rule.right)

                    # Swap the left and right page_numbers
                    self.page_numbers[left_index], self.page_numbers[right_index] = (
                        self.page_numbers[right_index],
                        self.page_numbers[left_index],
                    )

    @property
    def middle_page(self) -> int:
        return self.page_numbers[len(self.page_numbers) // 2]

    @property
    def is_valid(self) -> bool:
        return all([rule.check(self.page_numbers) for rule in self.rules])


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.

    """
    rules: list[Rule] = [
        Rule(left=int(line.split("|")[0]), right=int(line.split("|")[1]))
        for line in input_lines
        if "|" in line
    ]
    updates: list[Update] = [
        Update(page_numbers=[int(num) for num in line.split(",")], rules=rules)
        for line in input_lines
        if "," in line
    ]
    return sum([update.middle_page for update in updates if update.is_valid])


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    rules: list[Rule] = [
        Rule(left=int(line.split("|")[0]), right=int(line.split("|")[1]))
        for line in input_lines
        if "|" in line
    ]
    updates: list[Update] = [
        Update(page_numbers=[int(num) for num in line.split(",")], rules=rules)
        for line in input_lines
        if "," in line
    ]
    # Filter out the updates that are valid
    updates = [update for update in updates if not update.is_valid]
    for update in updates:
        update.fix_order()
    return sum([update.middle_page for update in updates if update.is_valid])


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_5.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
