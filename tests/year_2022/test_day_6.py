from challenges.year_2022.day_6 import part_one, part_two

TEST_INPUT_1: str = "bvwbjplbgvbhsrlpgdmjqwftvncz"
TEST_INPUT_2: str = "nppdvjthqldpwncqszvftbrmjlhg"
TEST_INPUT_3: str = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
TEST_INPUT_4: str = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"


def test_part_one():
    """Test based on the example provided in the challenge."""

    assert part_one(TEST_INPUT_1) == 5
    assert part_one(TEST_INPUT_2) == 6
    assert part_one(TEST_INPUT_3) == 10
    assert part_one(TEST_INPUT_4) == 11


TEST_INPUT_5 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
TEST_INPUT_6 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
TEST_INPUT_7 = "nppdvjthqldpwncqszvftbrmjlhg"
TEST_INPUT_8 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
TEST_INPUT_9 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"


def test_part_two():
    """Test based on the example provided in the challenge."""

    assert part_two(TEST_INPUT_5) == 19
    assert part_two(TEST_INPUT_6) == 23
    assert part_two(TEST_INPUT_7) == 23
    assert part_two(TEST_INPUT_8) == 29
    assert part_two(TEST_INPUT_9) == 26
