from aoc.year_2022.day_13 import part_one, part_two

TEST_INPUT: list[str] = [
    "[1,1,3,1,1]",
    "[1,1,5,1,1]",
    "",
    "[[1],[2,3,4]]",
    "[[1],4]",
    "",
    "[9]",
    "[[8,7,6]]",
    "",
    "[[4,4],4,4]",
    "[[4,4],4,4,4]",
    "",
    "[7,7,7,7]",
    "[7,7,7]",
    "",
    "[]",
    "[3]",
    "",
    "[[[]]]",
    "[[]]",
    "",
    "[1,[2,[3,[4,[5,6,7]]]],8,9]",
    "[1,[2,[3,[4,[5,6,0]]]],8,9]",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 13


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 140
