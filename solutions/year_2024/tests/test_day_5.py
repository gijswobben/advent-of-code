from day_5 import part_one, part_two

TEST_INPUT: list[str] = [
    "47|53",
    "97|13",
    "97|61",
    "97|47",
    "75|29",
    "61|13",
    "75|53",
    "29|13",
    "97|29",
    "53|29",
    "61|53",
    "97|53",
    "61|29",
    "47|13",
    "75|47",
    "97|75",
    "47|61",
    "75|61",
    "47|29",
    "75|13",
    "53|13",
    "",
    "75,47,61,53,29",
    "97,61,53,29,13",
    "75,29,13",
    "75,97,47,61,53",
    "61,13,29",
    "97,13,75,29,47",
]


def test_part_one() -> None:
    """Test based on the example provided in the challenge."""
    result = part_one(TEST_INPUT)
    assert result == 143


def test_part_two() -> None:
    """Test based on the example provided in the challenge."""
    result = part_two(TEST_INPUT)
    assert result == 123
