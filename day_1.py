from typing import Generator


def test_elves_calories():
    test_input = [
        "1000",
        "2000",
        "3000",
        "",
        "4000",
        "",
        "5000",
        "6000",
        "",
        "7000",
        "8000",
        "9000",
        "",
        "10000",
    ]

    result = sorted(elves_calories(test_input), reverse=True)
    assert max(result) == 24000
    assert sum(result[:3]) == 45000


def elves_calories(input_lines: list[str]) -> Generator[int, None, None]:
    """Method that combines groups of lines, separated by an empty line,
    and sums the results.

    Args:
        input_lines (list[str]): list of strings with one number by line
            and blank lines as separator.

    Returns:
        list[int]: list of total calories per elve.
    """
    result: list[int] = []
    buffer: int = 0
    for line in input_lines:
        if line == "":
            result.append(buffer)
            yield buffer
            buffer = 0
        else:
            buffer += int(line)
    result.append(buffer)
    yield buffer
    # return result


if __name__ == "__main__":

    # Read the dta
    with open("day_1.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    result = sorted(elves_calories(input_lines), reverse=True)
    print("Part one:", max(result))
    print("Part two:", result[0] + result[1] + result[2])
