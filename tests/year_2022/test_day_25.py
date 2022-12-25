from aoc.year_2022.day_25 import part_one, part_two

TEST_INPUT: list[str] = [
    "1=-0-2",
    "12111",
    "2=0=",
    "21",
    "2=01",
    "111",
    "20012",
    "112",
    "1=-1=",
    "1-12",
    "12",
    "1=",
    "122",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == "2=-1=0"


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 0
