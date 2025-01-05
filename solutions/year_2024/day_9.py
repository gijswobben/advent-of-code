"""Assignment for day 9 of 2024 Advent of Code.

https://adventofcode.com/2024/day/9
"""

from pathlib import Path


class Block:
    def __init__(self, size: int, identifier: int | None = None) -> None:
        self.size = size
        self.identifier = identifier

    def __repr__(self) -> str:
        if self.is_free:
            return f"Free({self.size})"
        return f"Block(id={self.identifier}, size={self.size})"

    @property
    def is_free(self) -> bool:
        return self.identifier is None


class DiskMap:
    """A class to represent a disk map.

    Args:
    ----
        input_line: The input line.

    """

    def __init__(self, input_line: str) -> None:
        self.input_line: list[int] = [int(char) for char in input_line]
        self.blocks: list[Block] = []
        identifier = 0
        for index, value in enumerate(self.input_line):
            if index % 2 == 0:
                self.blocks.append(Block(value, identifier=identifier))
                identifier += 1
            else:
                if value > 0:
                    self.blocks.append(Block(value))

    def _merge_empty_blocks(self, blocks: list[Block]) -> list[Block]:
        merged_blocks: list[Block] = [blocks.pop(0)]
        for block in blocks:
            if block.is_free and merged_blocks[-1].is_free:
                merged_blocks[-1].size += block.size
            else:
                merged_blocks.append(block)
        return merged_blocks

    def compact_files(self) -> list[Block]:
        """Compact the files on the disk.

        Move files as a whole. Do not split files.
        """
        # Files in reverse order of identifier
        files: list[Block] = [
            block for block in self.blocks if block.identifier is not None
        ][1:]
        files.sort(
            key=lambda b: b.identifier if b.identifier is not None else -1,
            reverse=True,
        )

        # Loop the files in reverse order
        blocks = self.blocks.copy()
        for file in files:
            # Find the location of the file
            file_index = blocks.index(file)

            # Find the leftmost free space that is large enough to fit
            # the file and is left of the file itself
            for index, block in enumerate(blocks[:file_index]):
                if block.is_free:
                    # If the free block has the same size as the file
                    # block we can replace it and drop the file block
                    if block.size == file.size:
                        blocks[index] = file
                        blocks[file_index] = Block(size=block.size)
                        # Stop iterating since we found a match
                        break

                    # If the free block is larger than the file block we
                    # can split the free block into two blocks; 1 that
                    # contains the file and 1 that contains the
                    # remaining free space
                    elif block.size > file.size:
                        blocks = (
                            blocks[:index]
                            + [
                                file,  # File block
                                Block(block.size - file.size),  # Free space block
                            ]
                            + blocks[index + 1 : file_index]
                            + [
                                Block(file.size),  # Empty block where the file was
                            ]
                            + blocks[file_index + 1 :]
                        )
                        # Stop iterating since we found a match
                        break

            blocks = self._merge_empty_blocks(blocks)

        return blocks

    def compact_blocks(self) -> list[Block]:
        """Compact the blocks on the disk."""
        compacted_blocks: list[Block] = []
        original_blocks = self.blocks.copy()
        while True:
            # Pop all blocks from the left that are filled
            while original_blocks and not original_blocks[0].is_free:
                compacted_blocks.append(original_blocks.pop(0))

            # Pop all blocks from the right that are free
            while original_blocks and original_blocks[-1].is_free:
                original_blocks.pop()

            # Stop if no more blocks left
            if not original_blocks:
                break

            # Get the leftmost and rightmost blocks
            leftmost_block = original_blocks.pop(0)
            rightmost_block = original_blocks.pop()

            # If the blocks are the same size we can move them as a
            # whole
            if leftmost_block.size == rightmost_block.size:
                compacted_blocks.append(rightmost_block)

            # If the leftmost block is larger than the rightmost block
            # we can split the leftmost block into two blocks; 1 that
            # contains the rightmost block and 1 that contains the
            # remaining free space
            elif leftmost_block.size > rightmost_block.size:
                compacted_blocks.append(rightmost_block)
                original_blocks.insert(
                    0,
                    Block(leftmost_block.size - rightmost_block.size),
                )

            # If the rightmost block is larger than the leftmost block
            # we can split the rightmost block into two blocks; 1 that
            # contains the leftmost block and 1 that contains the
            # remaining file
            else:
                compacted_blocks.append(
                    Block(leftmost_block.size, identifier=rightmost_block.identifier),
                )
                original_blocks.append(
                    Block(
                        rightmost_block.size - leftmost_block.size,
                        identifier=rightmost_block.identifier,
                    ),
                )

        return compacted_blocks

    def expand(self, blocks: list[Block]) -> list[int]:
        """Expand the blocks to a list of identifiers.

        Args:
        ----
            blocks: The blocks to expand.

        Returns:
        -------
            The expanded list of identifiers.

        """
        output = []
        for block in blocks:
            if block.is_free:
                output.extend([0] * block.size)
            else:
                output.extend([block.identifier] * block.size)
        return output

    def checksum(self, blocks: list[Block]) -> int:
        """Calculate the checksum of the blocks.

        Args:
        ----
            blocks: The blocks to calculate the checksum for.

        Returns:
        -------
            The checksum.

        """
        line = self.expand(blocks)
        return sum(
            [index * value for index, value in enumerate(line)],
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
    diskmap = DiskMap(input_lines[0])
    compacted_blocks = diskmap.compact_blocks()
    return diskmap.checksum(compacted_blocks)


def part_two(input_lines: list[str]) -> int:
    """Produce results for assignment two.

    Args:
    ----
        input_lines (list[str]): The input lines (strings).

    Returns:
    -------
        int: The result for assignment two.

    """
    diskmap = DiskMap(input_lines[0])
    compacted_blocks = diskmap.compact_files()
    return diskmap.checksum(compacted_blocks)


if __name__ == "__main__":
    # Read the input
    with open(Path(__file__).parent / "data//day_9.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result = part_two(input_lines)
    print("Part two:", result)
