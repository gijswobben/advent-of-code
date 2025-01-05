from aoc.year_2021.day_16 import part_one, part_two

TEST_INPUT_ONE: list[str] = ["8A004A801A8002F478"]
TEST_INPUT_TWO: list[str] = ["620080001611562C8802118E34"]
TEST_INPUT_THREE: list[str] = ["C0015000016115A2E0802F182340"]
TEST_INPUT_FOUR: list[str] = ["A0016C880162017C3686B18A3D4780"]


def test_part_one():
    """Test based on the example provided in the challenge."""

    result = part_one(TEST_INPUT_ONE)
    assert result == 16
    result = part_one(TEST_INPUT_TWO)
    assert result == 12
    result = part_one(TEST_INPUT_THREE)
    assert result == 23
    result = part_one(TEST_INPUT_FOUR)
    assert result == 31


def test_part_two():
    """Test based on the example provided in the challenge."""

    result = part_two(["C200B40A82"])
    assert result == 3
    result = part_two(["04005AC33890"])
    assert result == 54
    result = part_two(["880086C3E88112"])
    assert result == 7
    result = part_two(["CE00C43D881120"])
    assert result == 9
