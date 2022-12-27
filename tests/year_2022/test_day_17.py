from aoc.year_2022.day_17 import part_one, part_two

TEST_INPUT: list[str] = [
    ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 3068


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 1514285714288
