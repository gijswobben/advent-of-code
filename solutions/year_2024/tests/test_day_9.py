from day_9 import part_one, part_two

TEST_INPUT: list[str] = [
    "2333133121414131402",
]
TEST_INPUT_1: list[str] = [
    "12345",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT_1)
    assert result == 60
    result = part_one(TEST_INPUT)
    assert result == 1928


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 2858
