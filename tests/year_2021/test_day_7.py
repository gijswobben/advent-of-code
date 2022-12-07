from challenges.year_2021.day_7 import part_one, part_two

TEST_INPUT: list[str] = ["16,1,2,0,4,2,7,1,2,14"]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 37


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 168
