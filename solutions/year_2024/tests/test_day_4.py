from day_4 import WordSearch, part_one, part_two

TEST_INPUT: list[str] = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]

TEST_INPUT_ALT = [
    "....XXMAS.",
    ".SAMXMS...",
    "...S..A...",
    "..A.A.MS.X",
    "XMASAMX.MM",
    "X.....XA.A",
    "S.S.S.S.SS",
    ".A.A.A.A.A",
    "..M.M.M.MM",
    ".X.X.XMASX",
]

TEST_INPUT_MINI = [
    "M.S",
    ".A.",
    "M.S",
]


def test_flip() -> None:
    assert WordSearch.flip_grid_90(["ab", "cd"]) == ["ca", "db"]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT_ALT)
    assert result == 18
    result = part_one(TEST_INPUT)
    assert result == 18


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT_MINI)
    assert result == 1
    result = part_two(TEST_INPUT)
    assert result == 9
