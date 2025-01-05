from day_6 import part_one, part_two

TEST_INPUT: list[str] = ["3,4,3,1,2"]


def test_part_one():
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 5934


def test_part_two():
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 26984457539
