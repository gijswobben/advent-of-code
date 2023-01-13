# https://adventofcode.com/2021/day/20

from __future__ import annotations

import itertools
from copy import deepcopy
from enum import IntEnum
from pathlib import Path


class Pixel(IntEnum):
    """Represents the states of a pixel."""

    DARK = 0
    LIGHT = 1


class Image:
    """Represents an image.

    Images can be enhanced using an enhancement algorithm.

    Args:
        enhancement_algorithm (list[Pixel]): The enhancement algorithm
            as a list of pixel colors.
        input_image (list[list[Pixel]]): The input image as a 2D array
            of pixels.
    """

    def __init__(
        self, enhancement_algorithm: list[Pixel], input_image: list[list[Pixel]]
    ) -> None:
        self.enhancement_algorithm = enhancement_algorithm
        self.image = input_image

        # The color of the rest of the space, outside the known image
        self._color_infinity = Pixel.DARK

    def padding(self, n: int = 1, pixel: Pixel = Pixel.DARK) -> None:
        """Pad the current image N times with a specific color.

        Args:
            n (int, optional): The number of pixels to pad. Defaults to
                1.
            pixel (Pixel, optional): The pixel color to use for padding.
                Defaults to Pixel.DARK.
        """

        padding = [pixel for _ in range(n)]
        for index in range(len(self.image)):
            self.image[index] = [*padding, *self.image[index], *padding]
        for _ in range(n):
            self.image.insert(0, [pixel for _ in range(len(self.image[0]))])
            self.image.append([pixel for _ in range(len(self.image[0]))])

    def strip(self, n: int = 1) -> None:
        """Strip N pixels off the image.

        Args:
            n (int, optional): The number of pixels to remove. Defaults
                to 1.
        """
        self.image = self.image[n:-n]
        self.image = [row[n:-n] for row in self.image]

    @property
    def n_light_pixels(self) -> int:
        """The number of light pixels in the image.

        Raises:
            Exception: Raised when the pixel color of infinity is
                Pixel.LIGHT. This would result in an infinite number of
                light pixels.

        Returns:
            int: The number of ligth pixels.
        """
        if self._color_infinity == Pixel.LIGHT:
            raise Exception("Infinity color is LIGHT.")
        return sum(itertools.chain.from_iterable(self.image))

    def enhance(self) -> Image:
        """Enhance the image using the enhancement algorithm.

        Returns:
            Image: This image, enhanced.
        """

        # Add pixels around the edge in the infinity color
        self.padding(n=2, pixel=self._color_infinity)

        # Relative pixels (NOTE: Order matters)
        relative_positions: list[tuple[int, int]] = [
            # First row
            (-1, -1),
            (0, -1),
            (1, -1),
            # Second row
            (-1, 0),
            (0, 0),
            (1, 0),
            # Third row
            (-1, 1),
            (0, 1),
            (1, 1),
        ]

        # Work on a copy of the original image
        image = deepcopy(self.image)

        # Loop all pixels (ignore the outmost pixels because those are
        # just padding)
        for row in range(1, len(image) - 1):
            for column in range(1, len(image[0]) - 1):

                # Get all relative positions
                binary = "".join(
                    [
                        str(image[row + y][column + x].value)
                        for x, y in relative_positions
                    ]
                )

                # Replace the pixel in the original image with the new
                # value
                self.image[row].pop(column)
                self.image[row].insert(
                    column, self.enhancement_algorithm[int(binary, 2)]
                )

        # Check if infinity changed color
        self._color_infinity = self.enhancement_algorithm[
            int("".join(str(self._color_infinity.value) for _ in range(9)), 2)
        ]

        # Strip away the extra padding
        self.strip()

        return self

    def __repr__(self) -> str:
        return "\n".join(
            "".join(["#" if pixel.value == 1 else "." for pixel in row])
            for row in self.image
        )


def part_one(input_lines: list[str]) -> int:

    # Parse the image
    image = Image(
        enhancement_algorithm=[
            Pixel.LIGHT if pixel == "#" else Pixel.DARK for pixel in input_lines[0]
        ],
        input_image=[
            [Pixel.LIGHT if pixel == "#" else Pixel.DARK for pixel in line]
            for line in input_lines[2:]
        ],
    )

    # Run image enhancement twice
    for _ in range(2):
        image.enhance()

    # Return the number of light pixels
    return image.n_light_pixels


def part_two(input_lines: list[str]) -> int:

    # Parse the image
    image = Image(
        enhancement_algorithm=[
            Pixel.LIGHT if pixel == "#" else Pixel.DARK for pixel in input_lines[0]
        ],
        input_image=[
            [Pixel.LIGHT if pixel == "#" else Pixel.DARK for pixel in line]
            for line in input_lines[2:]
        ],
    )

    # Run image enhancement twice
    for _ in range(50):
        image.enhance()

    # Return the number of light pixels
    return image.n_light_pixels


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2021/day_20.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)


# 5100 too high
