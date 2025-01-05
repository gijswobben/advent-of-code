from day_7 import part_one, part_two

TEST_INPUT: list[str] = [
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 3749


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 11387
