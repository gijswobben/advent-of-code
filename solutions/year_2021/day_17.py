# https://adventofcode.com/2021/day/17

import re
from dataclasses import dataclass
from pathlib import Path

import z3
from scipy.optimize import minimize


@dataclass()
class Position:
    x: int
    y: int


@dataclass()
class Velocity:
    x: int
    y: int


class Probe:
    def __init__(self, target_area: tuple[Position, Position]) -> None:
        self.target_area = target_area  # Top left, Bottom right
        print(self.target_area)

    def find_optimal_velocity(self) -> Velocity:

        for y in range(200, -200, -1):
            for x in range(200):
                path = self.simulate(x, y)
                if path is not None:
                    return Velocity(x, y)

    # def find_all_options(self) -> list[Velocity]:
    #     options: list[Velocity] = []
    #     for y in range(200, -200, -1):
    #         for x in range(-200, 200):
    #             path = self.simulate(x, y)
    #             if path is not None:
    #                 options.append(Velocity(x, y))
    #     return options

    def find_all_options(self) -> list[Velocity]:
        solver = z3.Optimize()
        velocity_x, velocity_y, x, y, time = z3.Ints("velocity_x velocity_y x y time")

        # Time should be positive
        solver.add(time >= 0)

        solver.add(x >= 0)
        solver.add(y >= 0)  # TODO: REMOVE

        # Should end up in the target area
        solver.add(x >= self.target_area[0].x, x <= self.target_area[1].x)
        solver.add(y >= self.target_area[0].y, y <= self.target_area[1].y)

        # Horizontal position is constraint by the initial horizontal
        # speed and the drag
        drag = z3.If(velocity_x - time <= 0, 0, velocity_x - time)
        solver.add(x == 0.5 * -1 * time**2 + 2 * time)

        # Vertical position constraint by the initial vertical speed
        # (v0y) and the gravity (g = -1)
        # y = y0 + 1/2 * (v0y + vy) * t
        # vy = v0y - g * t
        solver.add(
            y == velocity_y + 0.5 * (velocity_y + (velocity_y - time)) * (time - 1)
        )

        solver.minimize(time)
        solver.check()

        model = solver.model()
        print(model)
        print(model[velocity_x])
        print(model[velocity_y])

        return []

    def simulate(self, velocity_x: int, velocity_y: int) -> list[Position] | None:
        velocity = Velocity(velocity_x, velocity_y)
        position = Position(0, 0)
        visited_positions: list[Position] = [position]
        while True:

            # Update position
            position = Position(position.x + velocity.x, position.y + velocity.y)
            visited_positions.append(position)

            # In the target area
            if (
                self.target_area[0].x <= position.x <= self.target_area[1].x
                and self.target_area[0].y <= position.y <= self.target_area[1].y
            ):
                return visited_positions

            # Overshot
            elif (
                position.x > self.target_area[1].x or position.y < self.target_area[1].y
            ):
                # print(visited_positions)
                return None

            # Apply drag
            if velocity.x < 0:
                velocity.x += 1
            elif velocity.x > 0:
                velocity.x -= 1

            # Apply gravity
            velocity.y -= 1


def part_one(input_lines: list[str]) -> int:
    match = re.search(
        r"x=(?P<x_min>-?\d+)\.\.(?P<x_max>-?\d+), y=(?P<y_min>-?\d+)\.\.(?P<y_max>-?\d+)",
        input_lines[0],
    )
    if match is None:
        raise Exception("Invalid input")

    x_min = int(match.group("x_min"))
    x_max = int(match.group("x_max"))
    y_min = int(match.group("y_min"))
    y_max = int(match.group("y_max"))
    top_left = Position(min(x_min, x_max), min(y_min, y_max))
    bottom_right = Position(max(x_min, x_max), max(y_min, y_max))

    probe = Probe(target_area=(top_left, bottom_right))

    optimal_velocity = probe.find_optimal_velocity()

    path = probe.simulate(optimal_velocity.x, optimal_velocity.y)
    return max([p.y for p in path])


def part_two(input_lines: list[str]) -> int:
    match = re.search(
        r"x=(?P<x_min>-?\d+)\.\.(?P<x_max>-?\d+), y=(?P<y_min>-?\d+)\.\.(?P<y_max>-?\d+)",
        input_lines[0],
    )
    if match is None:
        raise Exception("Invalid input")

    x_min = int(match.group("x_min"))
    x_max = int(match.group("x_max"))
    y_min = int(match.group("y_min"))
    y_max = int(match.group("y_max"))
    top_left = Position(min(x_min, x_max), max(y_min, y_max))
    bottom_right = Position(max(x_min, x_max), min(y_min, y_max))
    print((top_left, bottom_right))

    probe = Probe(target_area=(top_left, bottom_right))

    optimal_velocity = probe.find_all_options()
    print(optimal_velocity)

    # test = [
    #     Velocity(23, -10),
    #     Velocity(25, -7),
    #     Velocity(8, 0),
    #     Velocity(26, -10),
    #     Velocity(20, -8),
    #     Velocity(25, -6),
    #     Velocity(25, -10),
    #     Velocity(8, 1),
    #     Velocity(24, -10),
    #     Velocity(7, 5),
    #     Velocity(23, -5),
    #     Velocity(27, -10),
    #     Velocity(8, -2),
    #     Velocity(25, -9),
    #     Velocity(26, -6),
    #     Velocity(30, -6),
    #     Velocity(7, -1),
    #     Velocity(13, -2),
    #     Velocity(15, -4),
    #     Velocity(7, 8),
    #     Velocity(22, -8),
    #     Velocity(23, -8),
    #     Velocity(23, -6),
    #     Velocity(24, -8),
    #     Velocity(7, 2),
    #     Velocity(27, -8),
    #     Velocity(27, -5),
    #     Velocity(25, -5),
    #     Velocity(29, -8),
    #     Velocity(7, 7),
    #     Velocity(7, 3),
    #     Velocity(9, -2),
    #     Velocity(11, -3),
    #     Velocity(13, -4),
    #     Velocity(30, -8),
    #     Velocity(28, -10),
    #     Velocity(27, -9),
    #     Velocity(30, -9),
    #     Velocity(30, -5),
    #     Velocity(29, -6),
    #     Velocity(6, 8),
    #     Velocity(20, -10),
    #     Velocity(8, -1),
    #     Velocity(28, -8),
    #     Velocity(15, -2),
    #     Velocity(26, -7),
    #     Velocity(7, 6),
    #     Velocity(7, 0),
    #     Velocity(10, -2),
    #     Velocity(30, -7),
    #     Velocity(21, -8),
    #     Velocity(22, -6),
    #     Velocity(11, -2),
    #     Velocity(6, 7),
    #     Velocity(21, -9),
    #     Velocity(29, -9),
    #     Velocity(12, -2),
    #     Velocity(7, 1),
    #     Velocity(28, -6),
    #     Velocity(9, -1),
    #     Velocity(11, -1),
    #     Velocity(28, -5),
    #     Velocity(22, -7),
    #     Velocity(21, -7),
    #     Velocity(20, -5),
    #     Velocity(6, 4),
    #     Velocity(6, 2),
    #     Velocity(15, -3),
    #     Velocity(28, -9),
    #     Velocity(23, -9),
    #     Velocity(11, -4),
    #     Velocity(10, -1),
    #     Velocity(20, -9),
    #     Velocity(21, -10),
    #     Velocity(24, -9),
    #     Velocity(24, -7),
    #     Velocity(9, 0),
    #     Velocity(29, -10),
    #     Velocity(6, 1),
    #     Velocity(20, -7),
    #     Velocity(22, -5),
    #     Velocity(12, -3),
    #     Velocity(6, 0),
    #     Velocity(12, -4),
    #     Velocity(26, -5),
    #     Velocity(14, -2),
    #     Velocity(7, 9),
    #     Velocity(20, -6),
    #     Velocity(27, -7),
    #     Velocity(6, 3),
    #     Velocity(14, -4),
    #     Velocity(30, -10),
    #     Velocity(26, -8),
    #     Velocity(24, -6),
    #     Velocity(22, -10),
    #     Velocity(26, -9),
    #     Velocity(22, -9),
    #     Velocity(29, -7),
    #     Velocity(6, 6),
    #     Velocity(6, 9),
    #     Velocity(24, -5),
    #     Velocity(28, -7),
    #     Velocity(21, -6),
    #     Velocity(14, -3),
    #     Velocity(25, -8),
    #     Velocity(23, -7),
    #     Velocity(27, -6),
    #     Velocity(7, 4),
    #     Velocity(6, 5),
    #     Velocity(13, -3),
    #     Velocity(21, -5),
    #     Velocity(29, -5),
    # ]
    # print(set([(v.x, v.y) for v in test]) - set([(v.x, v.y) for v in optimal_velocity]))

    # print(probe.simulate(7, -1))

    return len(optimal_velocity)


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_17.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
