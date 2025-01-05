from day_8 import part_one, part_two

TEST_INPUT_1: list[str] = [
    "..........",
    "..........",
    "..........",
    "....a.....",
    "........a.",
    ".....a....",
    "..........",
    "..........",
    "..........",
    "..........",
]

TEST_INPUT: list[str] = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT_1)
    assert result == 4
    result = part_one(TEST_INPUT)
    assert result == 14


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 34
