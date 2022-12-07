# https://adventofcode.com/2021/day/10

from pathlib import Path

OPENING_CHARACTERS = ["{", "(", "<", "["]
CLOSING_CHARACTERS = ["}", ")", ">", "]"]
CHARACTER_MAPPING = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


class SyntaxLine:
    def __init__(self, content: str) -> None:
        self.content = content
        self.error_character: str | None = None
        self.parse()

    def parse(self) -> None:

        # Make sure the first character is valid
        if self.content[0] in CLOSING_CHARACTERS:
            self.error_character = self.content[0]
            return None

        self.expected_close = [CHARACTER_MAPPING[self.content[0]]]
        for character in self.content[1:]:
            if character in OPENING_CHARACTERS:
                self.expected_close.append(CHARACTER_MAPPING[character])
            elif character != self.expected_close[-1]:
                self.error_character = character
                return None
            else:
                self.expected_close.pop(-1)
        return None

    @property
    def incomplete(self) -> bool:
        return not self.corrupt and len(self.expected_close) > 0

    @property
    def corrupt(self) -> bool:
        return self.error_character is not None


def score_syntax(input_lines: list[str]) -> int:
    lines: list[SyntaxLine] = [SyntaxLine(line) for line in input_lines]

    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    total = 0
    for line in [line for line in lines if line.corrupt]:
        total += points.get(
            line.error_character if line.error_character is not None else "", 0
        )

    return total


def completion_score(input_lines: list[str]) -> int:

    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    lines: list[SyntaxLine] = [SyntaxLine(line) for line in input_lines]
    scores: list[int] = []
    for line in [line for line in lines if line.incomplete]:
        completion = "".join(reversed(line.expected_close))
        score = 0
        for character in completion:
            score *= 5
            score += points[character]
        scores.append(score)

    return sorted(scores)[len(scores) // 2]


def part_one(input_lines: list[str]) -> int:
    score = score_syntax(input_lines=input_lines)
    return score


def part_two(input_lines: list[str]) -> int:
    score = completion_score(input_lines=input_lines)
    return score


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[2] / "data/year_2021/day_10.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
