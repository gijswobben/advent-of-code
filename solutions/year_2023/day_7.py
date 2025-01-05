"""Assignment for day 7 of 2023 Advent of Code.

https://adventofcode.com/2023/day/7
"""

from __future__ import annotations

from collections import Counter
from enum import IntEnum
from pathlib import Path
from typing import Any


class HandType(IntEnum):

    """Types of hands in a game."""

    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


class CardType(IntEnum):

    """Types of cards and their corresponding values."""

    CARD_A = 14
    CARD_K = 13
    CARD_Q = 12
    CARD_J = 11
    CARD_J_ALT = 1
    CARD_T = 10
    CARD_9 = 9
    CARD_8 = 8
    CARD_7 = 7
    CARD_6 = 6
    CARD_5 = 5
    CARD_4 = 4
    CARD_3 = 3
    CARD_2 = 2


class Hand:

    """An individual hand."""

    def __init__(
        self,
        cards: list[str],
        score: int,
        with_joker_rule: bool = False,
    ) -> None:
        """Create a hand of Camel Poker.

        Args:
        ----
            cards (list[str]): List of cards in the hand.
            score (int): The score for this hand.
            with_joker_rule (bool, optional): Whether or not to play
                with the new Joker rule. Defaults to False.
        """
        # Store the inputs
        self.cards: list[str] = cards
        self.score = score
        self.with_joker_rule = with_joker_rule

        # Map the cards to individual values
        self.card_values: list[CardType] = [CardType[f"CARD_{card}"] for card in cards]

        # Replace jokers with the alternative points for jokers
        if with_joker_rule:
            self.card_values = [
                card if card != CardType.CARD_J else CardType.CARD_J_ALT
                for card in self.card_values
            ]

    @property
    def type(self) -> HandType:
        """The type of this hand."""
        # Get counts of the individual cards
        counter = Counter(self.cards)

        # Check for five of a kind (can also be 5 Jokers)
        if len(counter) == 1:
            return HandType.FIVE_OF_A_KIND

        # Apply the Joker rule if needed
        if self.with_joker_rule:
            # Make the Joker count for the most common card in the hand
            most_common = [
                counts for counts in counter.most_common() if counts[0] != "J"
            ]
            j_card_count = counter["J"]
            counter[most_common[0][0]] += j_card_count
            del counter["J"]

        # Check for five of a kind (again because we modified the Joker
        # card)
        if len(counter) == 1:
            return HandType.FIVE_OF_A_KIND
        # Check for four of a kind
        elif len(counter) == 2 and max(counter.values()) == 4:
            return HandType.FOUR_OF_A_KIND
        # Check for full house
        elif len(counter) == 2 and max(counter.values()) == 3:
            return HandType.FULL_HOUSE
        # Check for three of a kind
        elif len(counter) == 3 and max(counter.values()) == 3:
            return HandType.THREE_OF_A_KIND
        # Check for two pair
        elif len(counter) == 3 and max(counter.values()) == 2:
            return HandType.TWO_PAIR
        # Check for one pair
        elif len(counter) == 4 and max(counter.values()) == 2:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    def _check_type(self, other: Hand | Any) -> None:
        """Verify the type of the "other".

        Args:
        ----
            other (Hand | Any): The other object to compare to.

        Raises:
        ------
            ValueError: When "other" is not a Hand object.
        """
        if not isinstance(other, Hand):
            raise ValueError("Can only compare hands to other hands.")

    def __lt__(self, other: Hand | Any) -> bool:
        """Compare objects of this class to other objects.

        Args:
        ----
            other (Hand | Any): The other to compare to.

        Raises:
        ------
            Exception: Raised when 2 hands are identical (should never
                be the case).
            ValueError: Raised when this object is compared to something
                other than a Hand.

        Returns:
        -------
            bool: True when this object has a lower value than other.
        """
        # Make sure the other is also a hand
        self._check_type(other)

        # Compare types
        if self.type < other.type:
            return True
        elif self.type > other.type:
            return False

        # Compare individual card values when the types are the same
        else:
            for self_card, other_card in zip(self.card_values, other.card_values):
                if self_card.value > other_card.value:
                    return True
                elif self_card.value < other_card.value:
                    return False
            raise Exception("Hands are identical")

    def __repr__(self) -> str:
        """Return string representation of this object."""
        return f"{''.join(self.cards)}"


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.
    """
    # Parse the input
    splits = [line.split(" ") for line in input_lines]
    hands = [Hand(cards=list(hand), score=int(score)) for hand, score in splits]

    # Sort the hands
    hands.sort(reverse=True)

    return sum(
        [rank * hand.score for rank, hand in zip(range(1, len(hands) + 1), hands)],
    )


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.
    """
    # Parse the input
    splits = [line.split(" ") for line in input_lines]
    hands = [
        Hand(cards=list(hand), score=int(score), with_joker_rule=True)
        for hand, score in splits
    ]

    # Sort the hands
    hands.sort(reverse=True)

    return sum(
        [rank * hand.score for rank, hand in zip(range(1, len(hands) + 1), hands)],
    )


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_7.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
