from day_6 import part_one, part_two

TEST_INPUT: list[str] = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 288


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 0
