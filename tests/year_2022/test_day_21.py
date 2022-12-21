from aoc.year_2022.day_21 import part_one, part_two

TEST_INPUT: list[str] = [
    "root: pppw + sjmn",
    "dbpl: 5",
    "cczh: sllz + lgvd",
    "zczc: 2",
    "ptdq: humn - dvpt",
    "dvpt: 3",
    "lfqf: 4",
    "humn: 5",
    "ljgn: 2",
    "sjmn: drzm * dbpl",
    "sllz: 4",
    "pppw: cczh / lfqf",
    "lgvd: ljgn * ptdq",
    "drzm: hmdt - zczc",
    "hmdt: 32",
]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT)
    assert result == 152


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(TEST_INPUT)
    assert result == 301
