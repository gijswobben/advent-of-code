from day_20 import part_one, part_two

TEST_INPUT: list[str] = [
    "1",
    "2",
    "-3",
    "3",
    "-2",
    "0",
    "4",
]


def test_part_one():
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 3


def test_part_two():
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 1623178306
