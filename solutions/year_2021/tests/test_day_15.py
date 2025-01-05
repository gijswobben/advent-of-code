from aoc.year_2021.day_15 import part_one, part_two

TEST_INPUT: list[str] = [
    "1163751742",
    "1381373672",
    "2136511328",
    "3694931569",
    "7463417111",
    "1319128137",
    "1359912421",
    "3125421639",
    "1293138521",
    "2311944581",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 40


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 315
