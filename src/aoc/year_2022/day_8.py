# https://adventofcode.com/2022/day/8

from __future__ import annotations

import functools
from enum import Enum
from pathlib import Path
from typing import Generator

import numpy as np


class Direction(Enum):
    """Possible (relative) directions to look into."""

    LEFT = (-1, 0)
    RIGHT = (1, 0)
    TOP = (0, -1)
    BOTTOM = (0, 1)


class Tree:
    """Class that represents a single tree.

    Args:
        x (int): The horizontal position of this tree in the forrest.
        y (int): The vertical position of this tree in the forrest.
        height (int): The height of this tree.
        forrest (Forrest): A reference to the forrest this tree belongs
            to.
    """

    def __init__(self, x: int, y: int, height: int, forrest: Forrest) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.forrest = forrest

    def get_neighbour(self, direction: Direction) -> Tree | None:
        """Get a neighbouring tree in a particular direction (if there
        is one).

        Args:
            direction (Direction): The direction to look in when getting
                the next tree.

        Returns:
            Tree | None: The resulting tree or None if this tree is next
                to the edge of the forrest.
        """
        return self.forrest.get_tree(
            self.x + direction.value[0], self.y + direction.value[1]
        )

    def get_line_of_sight(self, direction: Direction) -> list[Tree]:
        """Get all trees in a particular direction.

        Args:
            direction (Direction): The direction to look in when getting
                the next trees.

        Returns:
            list[Tree]: A list of trees in the chosen direction.
        """
        line: list[Tree] = []
        next_tree = self.get_neighbour(direction=direction)
        while next_tree is not None:
            line.append(next_tree)
            next_tree = next_tree.get_neighbour(direction=direction)
        return line

    @property
    def scenic_score(self) -> int:
        """Score that reflects the number of visible trees in all
        directions, relative to this tree.
        """

        def _filter_trees(trees: list[Tree]) -> list[Tree]:
            result: list[Tree] = []
            for tree in trees:
                if tree.height >= self.height:
                    result.append(tree)
                    break
                result.append(tree)
            return result

        viewing_distance_left = len(
            _filter_trees(self.get_line_of_sight(Direction.LEFT))
        )
        viewing_distance_right = len(
            _filter_trees(self.get_line_of_sight(Direction.RIGHT))
        )
        viewing_distance_top = len(_filter_trees(self.get_line_of_sight(Direction.TOP)))
        viewing_distance_bottom = len(
            _filter_trees(self.get_line_of_sight(Direction.BOTTOM))
        )

        return (
            viewing_distance_left
            * viewing_distance_right
            * viewing_distance_top
            * viewing_distance_bottom
        )

    @property
    def is_visible(self) -> bool:
        """Whether or not this tree is visible from the edge of the
        forrest.
        """

        # Trees along the edge are all visible
        if (
            self.x == self.forrest.width
            or self.y == self.forrest.height
            or self.x == 0
            or self.y == 0
        ):
            return True

        # Check the line of sight
        else:
            blocked_left = any(
                [
                    self.height <= tree.height
                    for tree in self.get_line_of_sight(Direction.LEFT)
                ]
            )
            blocked_right = any(
                [
                    self.height <= tree.height
                    for tree in self.get_line_of_sight(Direction.RIGHT)
                ]
            )
            blocked_top = any(
                [
                    self.height <= tree.height
                    for tree in self.get_line_of_sight(Direction.TOP)
                ]
            )
            blocked_bottom = any(
                [
                    self.height <= tree.height
                    for tree in self.get_line_of_sight(Direction.BOTTOM)
                ]
            )

            # If views from all directions are blocked, this treee is
            # visible
            if all([blocked_left, blocked_right, blocked_top, blocked_bottom]):
                return False
            else:
                return True


class Forrest:
    """Class that represents a forrest of trees."""

    def __init__(self) -> None:
        self.trees: list[Tree] = []

    @property
    def width(self) -> int:
        """The width of the forrest as the largest x position."""
        return max([tree.x for tree in self])

    @property
    def height(self) -> int:
        """The height of the forrest as the largest y position."""
        return max([tree.y for tree in self])

    def get_tree(self, x: int, y: int) -> Tree | None:
        """Get an individual tree from it's position.

        Args:
            x (int): The x position of the tree.
            y (int): The y position of the tree.

        Returns:
            Tree | None: The requested tree or None if there is no tree
                at the selected position.
        """
        return next((tree for tree in self if tree.x == x and tree.y == y), None)

    def __iter__(self) -> Generator[Tree, None, None]:
        for tree in self.trees:
            yield tree

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Forrest:
        """Create a new Forrest object from a list of texts.

        Args:
            input_lines (list[str]): The lines of text, each containing
                a list of trees

        Returns:
            Forrest: The resulting Forrest object.
        """
        forrest = Forrest()
        trees: list[Tree] = []
        for y, line in enumerate(input_lines):
            for x, element in enumerate(list(line)):
                trees.append(Tree(x=x, y=y, height=int(element), forrest=forrest))
        forrest.trees = trees
        return forrest

    def print_visibility(self) -> None:
        """Print an overview of the forrest, indicating which trees are
        visible.
        """
        output: list[str] = []
        for y in range(self.height + 1):
            line = [tree for tree in self.trees if tree.y == y]
            line.sort(key=lambda tree: tree.x)
            output.append(" ".join([str(tree.is_visible)[0] for tree in line]))
        print("\n".join(output))


class ForrestV2:
    """High performance version of the Forrest class.

    This implementation doesn't make individual trees but represents the
    forrest as a Numpy matrix.

    Args:
        trees (list[list[int]]): Multidimensional array of trees (grid).
    """

    def __init__(self, trees: list[list[int]]) -> None:
        self.grid = np.array(trees)

    @property
    def visible(self) -> np.ndarray:
        """Numpy array of the same shape as the forrest. 1 indicates a
        tree is visible, 0 indicates a tree is not visible.
        """

        # Default: Everything is invisible
        visible = np.zeros_like(self.grid)

        # Loop all trees
        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                height = self.grid[y, x]

                # Get trees in all directions
                left = self.grid[y, :x]
                right = self.grid[y, x + 1 :]
                top = self.grid[:y, x]
                bottom = self.grid[y + 1 :, x]
                all_directions = [left, right, top, bottom]

                # If a tree is on the edge, it is visible
                if any([len(direction) == 0 for direction in all_directions]):
                    visible[y, x] = 1

                # If the tallest tree is lower than this tree, it is
                # visible
                elif any([max(direction) < height for direction in all_directions]):
                    visible[y, x] = 1

        return visible

    @property
    def scenic_scores(self) -> np.ndarray:
        """Numpy array of the same shape as the forrest. Each value
        represents the "Scenic score" for a tree in that particular
        place of the grid.
        """

        # Default: Everything is zero
        scores = np.zeros_like(self.grid)

        # Loop all trees
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                height = self.grid[y, x]

                # Get trees in all directions
                left = np.flip(self.grid[y, :x])
                if len(left) > 0 and np.max(left) >= height:
                    left_index = int(np.argmax(height <= left))
                    left = left[: left_index + 1]
                right = self.grid[y, x + 1 :]
                if len(right) > 0 and np.max(right) >= height:
                    right_index = int(np.argmax(height <= right))
                    right = right[: right_index + 1]
                top = np.flip(self.grid[:y, x])
                if len(top) > 0 and np.max(top) >= height:
                    top_index = int(np.argmax(height <= top))
                    top = top[: top_index + 1]
                bottom = self.grid[y + 1 :, x]
                if len(bottom) > 0 and np.max(bottom) >= height:
                    bottom_index = int(np.argmax(height <= bottom))
                    bottom = bottom[: bottom_index + 1]

                all_directions = [
                    len(left),
                    len(right),
                    len(top),
                    len(bottom),
                ]

                scores[y, x] = functools.reduce(
                    lambda a, b: a * b,
                    all_directions,
                )

        return scores

    @classmethod
    def from_text(self, input_lines: list[str]) -> ForrestV2:
        """Create a new Forrest object from a list of texts.

        Args:
            input_lines (list[str]): The lines of text, each containing
                a list of trees

        Returns:
            Forrest: The resulting ForrestV2 object.
        """
        trees: list[list[int]] = []
        for line in input_lines:
            tree_line: list[int] = []
            for element in line:
                tree_line.append(int(element))
            trees.append(tree_line)
        return ForrestV2(trees=trees)


def part_one(input_lines: list[str]) -> int:

    # Verbose and slow method, for educational purposes
    # forrest = Forrest.from_text(input_lines)
    # return len([tree for tree in forrest if tree.is_visible])

    # Faster Numpy array solution
    forrest = ForrestV2.from_text(input_lines)
    return np.sum(forrest.visible)


def part_two(input_lines: list[str]) -> int:

    # Verbose and slow method, for educational purposes
    # forrest = Forrest.from_text(input_lines)
    # return max([tree.scenic_score for tree in forrest])

    # Faster Numpy array solution
    forrest = ForrestV2.from_text(input_lines)
    return np.max(forrest.scenic_scores)


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_8.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
