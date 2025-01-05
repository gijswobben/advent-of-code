from aoc.year_2021.day_11 import part_one, part_two

TEST_INPUT: list[str] = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 1656


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 195
