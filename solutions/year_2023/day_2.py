"""Assignment for day 2 of 2023 Advent of Code.

https://adventofcode.com/2023/day/2
"""

import re
from collections import defaultdict
from pathlib import Path


def is_draw_valid(
    draw: str,
    total_red_cubes: int,
    total_green_cubes: int,
    total_blue_cubes: int,
) -> bool:
    """Check if a draw is valid.

    A draw is valid when the number of cubes of a color is less than or
    equal to the total number of cubes of that color.

    Args:
    ----
        draw (str): The draw to check.
        total_red_cubes (int): The total number of red cubes.
        total_green_cubes (int): The total number of green cubes.
        total_blue_cubes (int): The total number of blue cubes.

    Returns:
    -------
        bool: Whether the draw is valid.
    """
    # Start with zero cubes of each color
    colors: dict[str, int] = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }

    # Count the number of cubes of each color
    matches = re.findall(r"(?P<count>\d+)\s(?P<color>red|green|blue)", draw)
    for match in matches:
        colors[match[1]] = int(match[0])

    # Check if the draw is valid
    return all(
        [
            colors["red"] <= total_red_cubes,
            colors["green"] <= total_green_cubes,
            colors["blue"] <= total_blue_cubes,
        ],
    )


def part_one(input_lines: list[str]) -> int:
    """Produce results for assignment one.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment one.
    """
    # Given by the assignment
    total_red_cubes = 12
    total_green_cubes = 13
    total_blue_cubes = 14

    # Keep track of valid games
    valid_game_ids: list[int] = []

    # Check all the games
    for line in input_lines:
        # Extract the game id and draws
        game, rest = line.split(":")
        game_id = game.split(" ")[1]
        draws = rest.split(";")

        # Check if all draws are valid for this game
        if all(
            is_draw_valid(
                draw,
                total_red_cubes,
                total_green_cubes,
                total_blue_cubes,
            )
            for draw in draws
        ):
            # Add the game id to the list of valid game ids
            valid_game_ids.append(int(game_id))

    # Return the sum of all valid game ids
    return sum(valid_game_ids)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.
    """
    # Keep track of the power of all cubes
    cubes_power: list[int] = []

    # Check all the games
    for line in input_lines:
        # Extract the draws
        _, rest = line.split(":")
        draws = rest.split(";")

        # Extract the number of cubes of each color
        colors: dict[str, list[int]] = defaultdict(list)
        for draw in draws:
            matches = re.findall(r"(?P<count>\d+)\s(?P<color>red|green|blue)", draw)
            for match in matches:
                colors[match[1]].append(int(match[0]))

        # Determine the minimum number of cubes of each color needed
        min_red_cubes = max(colors["red"]) if len(colors["red"]) > 0 else 0
        min_green_cubes = max(colors["green"]) if len(colors["green"]) > 0 else 0
        min_blue_cubes = max(colors["blue"]) if len(colors["blue"]) > 0 else 0

        # Add the power of the cubes to the list
        cubes_power.append(min_red_cubes * min_green_cubes * min_blue_cubes)

    # Return the sum of all the power of the cubes
    return sum(cubes_power)


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2023/day_2.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
