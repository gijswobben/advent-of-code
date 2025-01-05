from day_10 import part_one, part_two

TEST_INPUT: list[str] = [
    ".....",
    ".S-7.",
    ".|.|.",
    ".L-J.",
    ".....",
]

TEST_INPUT_2: list[str] = [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ...",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 4

    result = part_one(TEST_INPUT_2)
    assert result == 8


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 0
