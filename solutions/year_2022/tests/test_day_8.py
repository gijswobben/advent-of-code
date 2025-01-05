from aoc.year_2022.day_8 import part_one, part_two

TEST_INPUT: list[str] = [
    "30373",
    "25512",
    "65332",
    "33549",
    "35390",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 21


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 8
