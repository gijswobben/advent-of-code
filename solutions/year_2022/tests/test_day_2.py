from day_2 import part_one, part_two

TEST_INPUT = [
    "A Y",
    "B X",
    "C Z",
]


def test_part_one():
    """Test based on the example provided in the challenge."""
    score = part_one(TEST_INPUT)
    assert score == 15


def test_part_two():
    """Test based on the example provided in the challenge."""
    score = part_two(TEST_INPUT)
    assert score == 12
