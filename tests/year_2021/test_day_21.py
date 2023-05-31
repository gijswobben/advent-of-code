from aoc.year_2021.day_21 import part_one, part_two

TEST_INPUT: list[str] = [
    "Player 1 starting position: 4",
    "Player 2 starting position: 8",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 739785


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 444356092776315
