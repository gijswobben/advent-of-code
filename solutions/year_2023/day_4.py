"""Assignment for day 4 of 2023 Advent of Code.

https://adventofcode.com/2023/day/4
"""

import re
from collections import deque
from pathlib import Path


class Card:

    """A scratch card."""

    def __init__(
        self,
        id: int,
        winning_numbers: list[int],
        your_numbers: list[int],
    ) -> None:
        """Create a new card.

        Args:
        ----
            id (int): The identifier of the card.
            winning_numbers (list[int]): The winning numbers.
            your_numbers (list[int]): Your numbers.
        """
        self.id = id
        self.winning_numbers = winning_numbers
        self.your_numbers = your_numbers

    @property
    def matching_numbers(self) -> list[int]:
        """The matching numbers.

        Returns
        -------
            list[int]: The matching numbers between the winning numbers
                and your numbers.
        """
        return [
            number for number in self.your_numbers if number in self.winning_numbers
        ]

    @property
    def score(self) -> int:
        """The score of the card.

        Returns
        -------
            int: The score of the card.
        """
        matching_numbers = self.matching_numbers
        if len(matching_numbers) == 0:
            return 0
        return int(2 ** (len(matching_numbers) - 1))


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.
    """
    # Pattern to parse a card
    pattern = re.compile(
        r"Card\s*(?P<card_id>\d+):\s*(?P<winning_numbers>(\d|\s)*)\|\s*(?P<your_numbers>(\d|\s)*)",
    )

    # Parse all the cards
    cards: list[Card] = []
    for line in input_lines:
        match = pattern.match(line)
        if match is None:
            raise Exception("Invalid input")

        cards.append(
            Card(
                id=int(match.group("card_id")),
                winning_numbers=[
                    int(number.strip())
                    for number in match.group("winning_numbers").split(" ")
                    if number.isdigit()
                ],
                your_numbers=[
                    int(number.strip())
                    for number in match.group("your_numbers").split(" ")
                    if number.isdigit()
                ],
            ),
        )

    return sum(card.score for card in cards)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.
    """
    # Pattern to parse a card
    pattern = re.compile(
        r"Card\s*(?P<card_id>\d+):\s*(?P<winning_numbers>(\d|\s)*)\|\s*(?P<your_numbers>(\d|\s)*)",
    )

    # Parse all the cards
    cards: dict[int, Card] = {}
    for line in input_lines:
        match = pattern.match(line)
        if match is None:
            raise Exception("Invalid input")

        cards[int(match.group("card_id"))] = Card(
            id=int(match.group("card_id")),
            winning_numbers=[
                int(number.strip())
                for number in match.group("winning_numbers").split(" ")
                if number.isdigit()
            ],
            your_numbers=[
                int(number.strip())
                for number in match.group("your_numbers").split(" ")
                if number.isdigit()
            ],
        )

    total_number_cards = 0
    queue = deque(cards.values())

    while len(queue) > 0:
        card = queue.popleft()
        total_number_cards += 1

        for index in range(card.id, card.id + len(card.matching_numbers)):
            queue.append(cards[index + 1])

    return total_number_cards


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_4.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
