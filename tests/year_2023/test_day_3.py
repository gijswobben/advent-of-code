from aoc.year_2023.day_3 import part_one, part_two

TEST_INPUT: list[str] = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 4361


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 467835
