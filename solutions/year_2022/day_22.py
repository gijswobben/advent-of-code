# https://adventofcode.com/2022/day/22

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Generator, Type, TypeVar

import numpy as np

_T = TypeVar("_T", bound="Map")


class Facing(IntEnum):
    """Direction in which we are facing."""

    RIGHT = 0
    BOTTOM = 1
    LEFT = 2
    TOP = 3


class DirectionChange(IntEnum):
    """Change of direction."""

    RIGHT = 1
    LEFT = -1


class Tile(IntEnum):
    """Contents of any of the tiles in the grid."""

    OPEN = 0
    WALL = 1
    VOID = 9  # Not on the map


@dataclass()
class Position:
    """Represents a position on the grid."""

    x: int
    y: int


class Map(ABC):
    """Base class for the Board or Cube.

    Args:
        board_map (list[list[int]]): List of lists representing each
            position on the map
        initial_facing (Facing, optional): Initial
            direction the user is facing. Defaults to Facing.RIGHT.
    """

    def __init__(
        self,
        board_map: list[list[int]],
        initial_facing: Facing = Facing.RIGHT,
        *args,
        **kwargs,
    ) -> None:
        self.facing = initial_facing

        # Create the map of the board
        self.map = np.full(
            [len(board_map), len(max(board_map, key=lambda x: len(x)))],
            Tile.VOID,
            dtype="int8",
        )
        for i, j in enumerate(board_map):
            self.map[i][0 : len(j)] = j

        # Set the initial position to the first open tile on the top row
        self.position: Position = Position(
            x=int(np.argmax(self.map[0, :] == Tile.OPEN)), y=0
        )

        # Keep track of the visited positions
        self.visited: list[Position] = []

    @classmethod
    def from_text(
        cls: Type[_T], input_lines: list[str], face_size: int | None = None
    ) -> _T:
        tile_map = {
            " ": Tile.VOID,
            ".": Tile.OPEN,
            "#": Tile.WALL,
        }
        board_map = [
            [tile_map[character].value for character in line] for line in input_lines
        ]
        return cls(board_map=board_map, face_size=face_size)

    def follow_instructions(self, instructions: Instructions):
        """Follow a set of instructions and move the user across the
        map.

        Args:
            instructions (Instructions): The instructions to follow.
        """

        facing_map = [facing.value for facing in Facing]
        for instruction in instructions:

            # Instruction to change direction
            if isinstance(instruction, DirectionChange):
                current_facing = facing_map.index(self.facing)
                new_facing = (current_facing + instruction) % (len(facing_map))
                self.facing = Facing(new_facing)

            # Instruction to take N steps in a direction
            else:
                for _ in range(instruction):
                    self.step()

    @abstractmethod
    def step(self) -> None:
        ...


class Board(Map):
    def step(self) -> None:
        """Take a single step across the board in the direction we're
        facing."""

        # Get the relative position by looking at the facing
        relative_next_position: Position = {
            Facing.RIGHT: Position(1, 0),
            Facing.BOTTOM: Position(0, 1),
            Facing.LEFT: Position(-1, 0),
            Facing.TOP: Position(0, -1),
        }[self.facing]

        # Get the coordinates of the next position
        next_position = Position(
            self.position.x + relative_next_position.x,
            self.position.y + relative_next_position.y,
        )

        # Off the map at the bottom
        if next_position.y >= self.map.shape[0]:
            next_position.y = int(np.argmax(self.map[:, next_position.x] != Tile.VOID))

        # Off the map at the top
        if next_position.y < 0:
            next_position.y = (
                self.map.shape[0]
                - 1
                - int(np.argmax(np.flip(self.map[:, next_position.x]) != Tile.VOID))
            )

        # Off the map on the right
        elif next_position.x >= self.map.shape[1]:
            next_position.x = int(np.argmax(self.map[next_position.y, :] != Tile.VOID))

        # Off the map at the left
        elif next_position.x < 0:
            next_position.x = (
                self.map.shape[1]
                - 1
                - int(np.argmax(np.flip(self.map[next_position.y, :]) != Tile.VOID))
            )

        # Walking into a void
        elif self.map[next_position.y, next_position.x] == Tile.VOID:
            if self.facing == Facing.RIGHT:
                next_position.x = int(
                    np.argmax(self.map[next_position.y, :] != Tile.VOID)
                )
            elif self.facing == Facing.LEFT:
                next_position.x = (
                    self.map.shape[1]
                    - 1
                    - int(np.argmax(np.flip(self.map[next_position.y, :]) != Tile.VOID))
                )
            elif self.facing == Facing.BOTTOM:
                next_position.y = int(
                    np.argmax(self.map[:, next_position.x] != Tile.VOID)
                )
            elif self.facing == Facing.TOP:
                next_position.y = (
                    self.map.shape[0]
                    - 1
                    - int(np.argmax(np.flip(self.map[:, next_position.x]) != Tile.VOID))
                )

        # Don't move if the next position is a wall
        if self.map[next_position.y, next_position.x] == Tile.WALL:
            pass

        # Move into the next position
        else:
            self.position = next_position

        self.visited.append(self.position)


class Face:
    """Represents a single face on a cube.

    Args:
        identifier (int): Face number (unique identifier).
        top_left (Position): Position of the top left corner of this
            face.
        bottom_right (Position): Position of the bottom right corner of
            this face.
    """

    def __init__(
        self,
        identifier: int,
        top_left: Position,
        bottom_right: Position,
    ) -> None:
        self.identifier = identifier
        self.top_left = top_left
        self.bottom_right = Position(x=bottom_right.x - 1, y=bottom_right.y - 1)
        self.size = bottom_right.x - top_left.x

    def contains(self, position: Position) -> bool:
        """Whether or not a position is on this face.

        Args:
            position (Position): The position to check.

        Returns:
            bool: True if the position is on this face.
        """

        return (
            position.x >= self.top_left.x
            and position.x <= self.bottom_right.x
            and position.y >= self.top_left.y
            and position.y <= self.bottom_right.y
        )

    def relative_x(self, position: Position) -> int:
        """Convert a postion to a relative position on this face.

        Args:
            position (Position): The position to translate.

        Raises:
            Exception: Raised when the position isn't on this face.

        Returns:
            int: The X position, relative to this face.
        """

        if not self.contains(position):
            raise Exception("Position not on this face")
        return self.right - position.x

    def relative_y(self, position: Position) -> int:
        """Convert a postion to a relative position on this face.

        Args:
            position (Position): The position to translate.

        Raises:
            Exception: Raised when the position isn't on this face.

        Returns:
            int: The Y position, relative to this face.
        """

        if not self.contains(position):
            raise Exception("Position not on this face")
        return self.bottom - position.y

    @property
    def top(self) -> int:
        return self.top_left.y

    @property
    def bottom(self) -> int:
        return self.bottom_right.y

    @property
    def left(self) -> int:
        return self.top_left.x

    @property
    def right(self) -> int:
        return self.bottom_right.x

    @property
    def bottom_left(self) -> Position:
        return Position(x=self.top_left.x, y=self.bottom_right.y)

    @property
    def top_right(self) -> Position:
        return Position(x=self.bottom_right.x, y=self.top_left.y)


class Cube(Map):
    """Represents the map as a cube.

    NOTE: This implementation supports only a single layout of the cube!
    It is hardcoded and works for my input, but it's not a generic
    solution.

    Args:
        board_map (list[list[int]]): List of lists representing each
            position on the map
        initial_facing (Facing, optional): Initial
            direction the user is facing. Defaults to Facing.RIGHT.
        face_size (int): The size of each face of the cube.
    """

    def __init__(
        self,
        board_map: list[list[int]],
        face_size: int,
        initial_facing: Facing = Facing.RIGHT,
    ) -> None:

        super().__init__(board_map, initial_facing)

        self.face_size = face_size

        # Create demarkations for all the "faces" of the cube
        # TODO: Make this work for different layouts of the cube
        self.face_1 = Face(
            identifier=1,
            top_left=Position(x=face_size, y=0),
            bottom_right=Position(x=2 * face_size, y=face_size),
        )
        self.face_2 = Face(
            identifier=2,
            top_left=Position(x=2 * face_size, y=0),
            bottom_right=Position(x=3 * face_size, y=face_size),
        )
        self.face_3 = Face(
            identifier=3,
            top_left=Position(x=face_size, y=face_size),
            bottom_right=Position(x=2 * face_size, y=2 * face_size),
        )
        self.face_4 = Face(
            identifier=4,
            top_left=Position(x=0, y=2 * face_size),
            bottom_right=Position(x=face_size, y=3 * face_size),
        )
        self.face_5 = Face(
            identifier=5,
            top_left=Position(x=face_size, y=2 * face_size),
            bottom_right=Position(x=2 * face_size, y=3 * face_size),
        )
        self.face_6 = Face(
            identifier=6,
            top_left=Position(x=0, y=3 * face_size),
            bottom_right=Position(x=face_size, y=4 * face_size),
        )
        self.faces = [
            self.face_1,
            self.face_2,
            self.face_3,
            self.face_4,
            self.face_5,
            self.face_6,
        ]

    def get_face(self, position: Position) -> Face:
        """Get the face that this position is located on.

        Args:
            position (Position): The position to find.

        Raises:
            Exception: Raised when the position isn't on any face.

        Returns:
            Face: The face that contains this position
        """

        for face in self.faces:
            if face.contains(position):
                return face
        raise Exception("Not found", position)

    def step(self) -> None:
        """Take a single step along the surface of the cube."""

        # Get the face number we're on
        face = self.get_face(self.position)

        width = self.map.shape[1]
        height = self.map.shape[0]

        # Get the relative position by looking at the facing
        relative_next_position: Position = {
            Facing.RIGHT: Position(1, 0),
            Facing.BOTTOM: Position(0, 1),
            Facing.LEFT: Position(-1, 0),
            Facing.TOP: Position(0, -1),
        }[self.facing]

        # Get the coordinates of the next position if we would continue
        # to move in the same direction
        next_position = Position(
            self.position.x + relative_next_position.x,
            self.position.y + relative_next_position.y,
        )
        next_facing = self.facing

        # Off the map at the top
        if next_position.y < 0:
            if face.identifier == 1:
                # Move to face 6
                next_position = Position(
                    x=self.face_6.left,
                    y=self.face_6.top
                    + (self.face_size - face.relative_x(self.position) - 1),
                )
                next_facing = Facing.RIGHT
            elif face.identifier == 2:
                # Move to face 6
                next_position = Position(
                    x=self.face_6.left
                    + (self.face_size - face.relative_x(self.position) - 1),
                    y=self.face_6.bottom,
                )
                next_facing = Facing.TOP
            else:
                raise Exception()

        # Off the map at the bottom
        if next_position.y >= height:
            if face.identifier == 6:
                # Move to face 2
                next_position = Position(
                    x=self.face_2.left
                    + (self.face_size - face.relative_x(self.position) - 1),
                    y=self.face_2.top,
                )
                next_facing = Facing.BOTTOM
            else:
                raise Exception()

        # Off the map on the right
        elif next_position.x >= width:
            if face.identifier == 2:
                # Move to face 5
                next_position = Position(
                    x=self.face_5.right,
                    y=self.face_5.top + face.relative_y(self.position),
                )
                next_facing = Facing.LEFT
            else:
                raise Exception()

        # Off the map at the left
        elif next_position.x < 0:
            if face.identifier == 4:
                # Move to face 1
                next_position = Position(
                    x=self.face_1.left,
                    y=self.face_1.top + face.relative_y(self.position),
                )
                next_facing = Facing.RIGHT
            elif face.identifier == 6:
                # Move to face 1
                next_position = Position(
                    x=self.face_1.left
                    + (self.face_size - face.relative_y(self.position) - 1),
                    y=self.face_1.top,
                )
                next_facing = Facing.BOTTOM
            else:
                raise Exception()

        # Walking into a void
        elif self.map[next_position.y, next_position.x] == Tile.VOID:
            if next_facing == Facing.RIGHT:
                if face.identifier == 3:
                    # To face 2
                    next_position = Position(
                        x=self.face_2.left
                        + (self.face_size - face.relative_y(self.position) - 1),
                        y=self.face_2.bottom,
                    )
                    next_facing = Facing.TOP
                elif face.identifier == 5:
                    # To face 2
                    next_position = Position(
                        x=self.face_2.right,
                        y=self.face_2.top + face.relative_y(self.position),
                    )
                    next_facing = Facing.LEFT
                elif face.identifier == 6:
                    # Move to face 5
                    next_position = Position(
                        x=self.face_5.left
                        + (self.face_size - face.relative_y(self.position) - 1),
                        y=self.face_5.bottom,
                    )
                    next_facing = Facing.TOP
                else:
                    raise Exception()

            elif next_facing == Facing.LEFT:
                if face.identifier == 1:
                    # To face 4
                    next_position = Position(
                        x=self.face_4.left,
                        y=self.face_4.top + face.relative_y(self.position),
                    )
                    next_facing = Facing.RIGHT
                elif face.identifier == 3:
                    # To face 4
                    next_position = Position(
                        x=self.face_4.left
                        + (self.face_size - face.relative_y(self.position) - 1),
                        y=self.face_4.top,
                    )
                    next_facing = Facing.BOTTOM
                else:
                    raise Exception()

            elif next_facing == Facing.BOTTOM:
                if face.identifier == 2:
                    # To face 3
                    next_position = Position(
                        x=self.face_3.right,
                        y=self.face_3.top
                        + (self.face_size - face.relative_x(self.position) - 1),
                    )
                    next_facing = Facing.LEFT
                elif face.identifier == 5:
                    # To face 6
                    next_position = Position(
                        x=self.face_6.right,
                        y=self.face_6.top
                        + (self.face_size - face.relative_x(self.position) - 1),
                    )
                    next_facing = Facing.LEFT
                else:
                    raise Exception()

            elif next_facing == Facing.TOP:
                if face.identifier == 4:
                    # To face 3
                    next_position = Position(
                        x=self.face_3.left,
                        y=self.face_3.top
                        + (self.face_size - face.relative_x(self.position) - 1),
                    )
                    next_facing = Facing.RIGHT
                else:
                    raise Exception()

        # Don't move if the next position is a wall
        if self.map[next_position.y, next_position.x] == Tile.WALL:
            pass

        # Move into the next position
        else:
            self.position = next_position
            self.facing = next_facing

        self.visited.append(self.position)


class Instructions:
    """Represents the instructions to follow.

    Args:
        instructions (list[int | DirectionChange]): List of
            instructions, either a numer of steps to take in the current
            direction, or a change of direction.
    """

    def __init__(self, instructions: list[int | DirectionChange]) -> None:
        self._instructions = instructions

    def __iter__(self) -> Generator[int | DirectionChange, None, None]:
        for instruction in self._instructions:
            yield instruction

    @classmethod
    def from_text(cls, input_text: str) -> Instructions:
        """Create a set of instructions from a string.

        Args:
            input_text (str): The string that contains the instructions.

        Returns:
            Instructions: The parsed Instructions object.
        """

        instructions: list[int | DirectionChange] = []
        buffer: list[str] = []
        for character in input_text:
            if character == "R":
                instructions.append(int("".join(buffer)))
                instructions.append(DirectionChange.RIGHT)
                buffer = []
            elif character == "L":
                instructions.append(int("".join(buffer)))
                instructions.append(DirectionChange.LEFT)
                buffer = []
            else:
                buffer.append(character)
        if buffer:
            instructions.append(int("".join(buffer)))
        return Instructions(instructions=instructions)


def part_one(input_lines: list[str]) -> int:

    # Get the instructions from the last line
    instructions = Instructions.from_text(input_lines[-1])

    # Parse the rest as the board
    board = Board.from_text(input_lines[:-1])

    # Follow the instructions on the board
    board.follow_instructions(instructions)

    # The final password is the sum of 1000 times the row, 4 times the
    # column, and the facing
    return (board.position.y + 1) * 1000 + (board.position.x + 1) * 4 + board.facing


def part_two(input_lines: list[str], face_size: int = 50) -> int:

    # Get the instructions from the last line
    instructions = Instructions.from_text(input_lines[-1])

    # Parse the rest as the cube
    cube = Cube.from_text(input_lines[:-1], face_size=face_size)

    # Follow the instructions on the cube
    cube.follow_instructions(instructions)

    # The final password is the sum of 1000 times the row, 4 times the
    # column, and the facing
    return (cube.position.y + 1) * 1000 + (cube.position.x + 1) * 4 + cube.facing


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_22.txt", "r") as f:
        input_lines = [
            line.strip("\n") for line in f.readlines() if line.strip("\n") != ""
        ]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
