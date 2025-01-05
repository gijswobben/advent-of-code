from day_3 import part_one, part_two

TEST_INPUT: list[str] = [
    "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))",
]
TEST_INPUT_2: list[str] = [
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 161


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT_2)
    assert result == 48
