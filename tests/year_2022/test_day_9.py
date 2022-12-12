from aoc.year_2022.day_9 import part_one, part_two

TEST_INPUT_ONE: list[str] = [
    "R 4",
    "U 4",
    "L 3",
    "D 1",
    "R 4",
    "D 1",
    "L 5",
    "R 2",
]

TEST_INPUT_TWO = [
    "R 5",
    "U 8",
    "L 8",
    "D 3",
    "R 17",
    "D 10",
    "L 25",
    "U 20",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT_ONE)
    assert result == 13


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT_ONE)
    assert result == 1

    result = part_two(TEST_INPUT_TWO)
    assert result == 36
