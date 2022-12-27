# https://adventofcode.com/2022/day/17

from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import Type

import numpy as np


class Chamber:
    """Represents a chamber with falling rocks.

    Args:
        jet_pattern (str): The pattern of the jet(s) in the room.
        width (int, optional): The width of the room. Defaults to 7.
    """

    def __init__(self, jet_pattern: str, width: int = 7) -> None:
        self.jet_pattern = list(jet_pattern)
        self.jet_pattern_position = 0
        self.width = width
        self.rock_generator = RockGenerator(
            pattern=[HorizontalRock, PlusRock, InverseLRock, VerticalRock, SquareRock]
        )
        self.grid = np.zeros((20_000, self.width))
        self._total_height = 0

    @property
    def top_of_rocks(self) -> int:
        """Position in the room that marks the top of the rock."""
        if np.all(self.grid == 0):
            return self.grid.shape[0]
        return int(np.argmax(np.any(self.grid > 0, axis=1) == True))

    @property
    def rock_height(self) -> int:
        """Total height of the rock."""
        return self.grid.shape[0] + self._total_height - self.top_of_rocks

    def mark_rock_on_grid(self, rock: Rock) -> np.ndarray:
        """Mark a particular rock, given its position, on the grid.

        Args:
            rock (Rock): The rock to mark on the internal grid.

        Returns:
            np.ndarray: The grid with the rock marked.
        """

        grid = self.grid.copy()
        for relative_position in rock.shape:
            y, x = (relative_position[0] + rock.y, relative_position[1] + rock.x)
            grid[y, x] = 1
        return grid

    def detect_pattern(self, pattern_size: int = 30) -> int | None:
        """Detect a pattern by looking for the top N lines in the rest
        of the grid.

        Args:
            pattern_size (int, optional): The chunk of the grid to
                consider a pattern. Defaults to 30.

        Returns:
            int | None: The position of the first repetition of the top
                N rows, or None if the top N rows are not repeated.
        """

        # Take the first N lines and consider them a "pattern"
        pattern = self.grid[
            self.top_of_rocks : self.top_of_rocks + pattern_size, :
        ].flatten()

        # Look for the pattern in the rest of the grid
        for i in range(
            self.top_of_rocks + pattern_size, self.grid.shape[0] - pattern_size
        ):
            window = self.grid[
                i : i + pattern_size,
                :,
            ].flatten()

            # Return the position of the first repetition if the window
            # equals the pattern
            if np.array_equal(window, pattern):
                return i

        return None

    def simulate(self, n_steps: int):
        """Simulate falling rocks for N periods.

        Args:
            n_steps (int): The number of periods to simulate.
        """

        top_of_rock_after_iteration: dict[int, int] = {}
        for iteration in range(n_steps):

            # Create a new rock and place it on the start position
            new_rock = next(self.rock_generator)
            new_rock.set_vertical_postion(y=self.top_of_rocks - new_rock.height - 3)
            new_rock.set_horizontal_position(2)

            # Let the rock fall into the chamber
            moving = True
            while moving:

                # Push by jet
                if self.jet_pattern[self.jet_pattern_position] == "<":
                    new_rock.move(chamber=self, relative_x=-1)
                else:
                    new_rock.move(chamber=self, relative_x=1)

                # Reset the pattern at the end
                self.jet_pattern_position += 1
                if self.jet_pattern_position >= len(self.jet_pattern):
                    self.jet_pattern_position = 0

                # Fall down
                moving = new_rock.move(chamber=self, relative_y=1)

            # Mark the new rock on the grid
            self.grid = self.mark_rock_on_grid(new_rock)

            # Store the position of the top of the rock at every
            # iteration so we can determine how much it grows in each
            # iteration
            top_of_rock_after_iteration[iteration] = self.top_of_rocks

            # After N iteration, look back to see if there is a pattern
            # we can repeat
            if iteration % 10_000 == 0 and iteration > 0:

                # Test if the last N lines are repeated somewhere
                pattern = self.detect_pattern(30)
                if pattern is not None:

                    # Determine how many iterations it takes for a
                    # pattern to repeat itself, and by how much the rock
                    # grows every iteration
                    iteration_of_last_pattern = min(
                        [
                            key
                            for key, value in top_of_rock_after_iteration.items()
                            if value == pattern
                        ]
                    )
                    repeats_every_n_iterations = iteration - iteration_of_last_pattern
                    rock_size_pattern = pattern - self.top_of_rocks

                    # Determine how much the rock will grow by repeating
                    # the pattern N times, then determine how much it
                    # will grow in the remaining iterations
                    remaining_iterations = n_steps - iteration
                    growth_by_repeating_pattern = (
                        remaining_iterations // repeats_every_n_iterations
                    ) * rock_size_pattern
                    growth_by_remaining_iterations = (
                        top_of_rock_after_iteration[iteration_of_last_pattern]
                        - top_of_rock_after_iteration[
                            iteration_of_last_pattern
                            + (remaining_iterations % repeats_every_n_iterations)
                        ]
                    )

                    # Store the total height after repeating the pattern
                    self._total_height = (
                        growth_by_repeating_pattern + growth_by_remaining_iterations - 1
                    )
                    break


class Rock(ABC):
    """Base class that represents a falling rock."""

    shape: list[tuple[int, int]]
    """Shape of this rock as a list of positions."""

    height: int
    width: int

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.stopped = False

    def set_vertical_postion(self, y: int):
        """Set the vertical position of this rock.

        Args:
            y (int): The vertical position to store.
        """
        self.y = y

    def set_horizontal_position(self, x: int):
        """Set the horizontal position of this rock.

        Args:
            y (int): The horizontal position to store.
        """
        self.x = x

    def move(self, chamber: Chamber, relative_x: int = 0, relative_y: int = 0) -> bool:
        """Move this rock in a particular chamber by a relative amount.

        Args:
            chamber (Chamber): The chamber to move in.
            relative_x (int, optional): The relative horizontal
                movement. Defaults to 0.
            relative_y (int, optional): The relative vertical movement.
                Defaults to 0.

        Returns:
            bool: Whether the rock moved. Is False if the rock couldn't
                move.
        """

        # Check the next positions down is blocked
        for relative_position in self.shape:
            y, x = (
                (relative_position[0] + self.y) + relative_y,
                (relative_position[1] + self.x) + relative_x,
            )

            if (
                x < 0
                or x >= chamber.grid.shape[1]
                or y >= chamber.grid.shape[0]
                or chamber.grid[y, x] == 1
            ):
                return False

        # Move is possible
        self.set_horizontal_position(x=self.x + relative_x)
        self.set_vertical_postion(y=self.y + relative_y)
        return True


class HorizontalRock(Rock):
    shape = [(0, x) for x in range(4)]
    height = 1
    width = 4


class PlusRock(Rock):
    shape = [*[(1, x) for x in range(3)], (0, 1), (2, 1)]
    height = 3
    width = 3


class InverseLRock(Rock):
    shape = [(0, 2), (1, 2), (2, 2), (2, 1), (2, 0)]
    height = 3
    width = 3


class VerticalRock(Rock):
    shape = [(y, 0) for y in range(4)]
    height = 4
    width = 1


class SquareRock(Rock):
    shape = [(0, 0), (0, 1), (1, 0), (1, 1)]
    height = 2
    width = 2


class RockGenerator:
    """Generator that produces an infinite stream of rocks, in a
    particular pattern.
    """

    def __init__(self, pattern: list[Type[Rock]]) -> None:
        self.pattern = pattern
        self.position = 0

    def __next__(self) -> Rock:
        next_rock = self.pattern[self.position]()
        self.position += 1
        if self.position >= len(self.pattern):
            self.position = 0
        return next_rock


def part_one(input_lines: list[str]) -> int:
    chamber = Chamber(jet_pattern=input_lines[0])
    chamber.simulate(n_steps=2022)
    return chamber.rock_height


def part_two(input_lines: list[str]) -> int:
    chamber = Chamber(jet_pattern=input_lines[0])
    chamber.simulate(n_steps=1_000_000_000_000)
    return chamber.rock_height


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_17.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
