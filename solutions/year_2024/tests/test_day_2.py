from day_2 import part_one, part_two

TEST_INPUT: list[str] = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 2


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 4
