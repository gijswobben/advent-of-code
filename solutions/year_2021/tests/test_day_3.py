from day_3 import part_one, part_two

TEST_INPUT: list[str] = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]


def test_part_one():
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 198


def test_part_two():
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 230
