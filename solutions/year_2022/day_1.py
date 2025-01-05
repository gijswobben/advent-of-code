# https://adventofcode.com/2022/day/1

from pathlib import Path


class Elf:
    def __init__(self, items: list[int] | None = None):
        self.items = items if items is not None else []

    def add_item(self, calories: int):
        self.items.append(calories)

    @property
    def total_calories(self) -> int:
        return sum(self.items)


def parse_input(input_lines: list[str]) -> list[Elf]:
    """Method that combines groups of lines, separated by an empty line,
    and creates elves from the result.

    Args:
        input_lines (list[str]): List of strings with one number by line
            and blank lines as separator.

    Returns:
        list[Elf]: List of Elves.
    """
    elves: list[Elf] = [Elf()]
    for line in input_lines:

        # Found a separator, all next items belong to the next elf
        if line == "":
            elves.append(Elf())

        # Add the number to the items of the last elf
        else:
            elves[-1].add_item(calories=int(line))

    return elves


def part_one(input_lines: list[str]) -> int:

    # Parse the input into a list of elves carrying items
    elves = parse_input(input_lines=input_lines)

    # Return the total calories from the elf with the most calories
    return max([elf.total_calories for elf in elves])


def part_two(input_lines: list[str]) -> int:

    # Parse the input into a list of elves carrying items
    elves = parse_input(input_lines=input_lines)

    # Sort the elves by total calories
    elves.sort(key=lambda elf: elf.total_calories, reverse=True)

    # Return the sum of the top 3
    return sum([elf.total_calories for elf in elves[:3]])


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_1.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output
    result = part_one(input_lines)
    print("Part one:", result)

    result = part_two(input_lines)
    print("Part two:", result)
