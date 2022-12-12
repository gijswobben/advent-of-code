# https://adventofcode.com/2022/day/10

from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import Callable


class Program:
    """A program is a set of instructions for the device CPU.

    Args:
        instructions (list[Command]): List of commands in this program.
    """

    def __init__(self, instructions: list[Command]) -> None:
        self.instructions: list[Command] = instructions

    @classmethod
    def from_text(cls, input_lines: list[str]) -> Program:
        """Parse text input into program instructions.

        Args:
            input_lines (list[str]): List of commands as strings.

        Raises:
            Exception: Raised when an invalid command is encountered.

        Returns:
            Program: The parsed Program object.
        """

        # Create a list of instructions (start whith a Noop because
        # Python uses 0 index lists)
        instructions: list[Command] = [Noop()]
        for line in input_lines:

            # Add a Noop
            if line.startswith("noop"):
                instructions.append(Noop())

            # Add an AddX command. Prefix with a Noop to simulate the
            # "duration" of the AddX command
            elif line.startswith("addx"):
                _, units_string = line.split(" ")
                instructions.append(Noop())
                instructions.append(AddX(int(units_string)))

            else:
                raise Exception("Invalid command in progam")

        # Return the program
        return Program(instructions=instructions)


class Device:
    """A device that has a CPU running a program, a clock that is
    responsible for triggering cycles and a display for showing the
    output.

    Args:
        program (Program): The instructions for the CPU as a program.
    """

    def __init__(self, program: Program) -> None:
        self.cpu = CPU(program=program)
        self.display = Display(cpu=self.cpu)

        # Create a clock that on every tick, calls the cycle methods of
        # the CPU and display
        self.clock = Clock(callbacks=[self.cpu.cycle, self.display.cycle])


class CPU:
    """A CPU that can execute a set of commands (program).

    Args:
        program (Program): The instructions for the CPU as a program.
    """

    def __init__(self, program: Program) -> None:
        self.program = program
        self.register_x = Register()

    def cycle(self, time: int) -> None:
        """Runs a single CPU cycle. During each cycle, the CPU executes
        a single line/command from the program.

        Args:
            time (int): The current time (from the clock).
        """

        # Get the next command and add it to the history of the
        # register
        next_command = self.program.instructions[time]
        self.register_x.history.append(next_command)


class Register:
    """Register that keeps track of a particular value (e.g. X)."""

    def __init__(self) -> None:
        self.history: list[Command] = []
        self._value = 1

    def get_value(self, time: int) -> int:
        """Get the value of the register at a particular time.

        Args:
            time (int): The time to retrieve the value from.

        Returns:
            int: The value of the register (initial value + all commands
                until this point in time).
        """
        return self._value + sum([command.units for command in self.history[:time]])


class Command(ABC):
    """Represents a single command to be executed."""

    def __init__(self, units: int = 0) -> None:
        self.units = units

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.units}>"


class Noop(Command):
    """Command that doesn't do anything but does consume the CPU for 1
    cycle.
    """

    ...


class AddX(Command):
    """Command that adds (or subtracts) a value from the registry. Takes
    2 CPU cycles to complete."""

    ...


class Clock:
    def __init__(self, callbacks: list[Callable[[int], None]]) -> None:
        self._callbacks = callbacks
        self._state = 0

    def tick(self):
        for callback in self._callbacks:
            callback(self._state)
        self._state += 1

    @property
    def time(self) -> int:
        return self._state


class Display:
    """A display that shows the outcome of the CPU instructions. Should
    display characters.

    Args:
        cpu (CPU): Reference to the CPU that drives this display.
        width (int, optional): The width of the display in characters.
            Defaults to 40.
        height (int, optional): The height of the display in characters.
            Defaults to 6.
    """

    def __init__(self, cpu: CPU, width: int = 40, height: int = 6) -> None:
        self.cpu = cpu
        self.width: int = width
        self.height: int = height
        self._state = [0] * self.width * self.height
        self.sprite_position = 1

    def cycle(self, time: int):
        """A full cycle of the display, triggered by a tick of the
        clock.

        Args:
            time (int): The current time (from the clock).
        """

        # Set the sprite position based on the value of the X register
        self.sprite_position = self.cpu.register_x.get_value(time + 1)

        # Get the position where the display wants to write
        remainder = time % self.width

        # If the position and sprite overlap, light up the position
        if (
            remainder == self.sprite_position
            or remainder == self.sprite_position - 1
            or remainder == self.sprite_position + 1
        ):
            self._state[time] = 1

    def render(self) -> str:
        """Render the state of the display as a string.

        Returns:
            str: The contents of the display.
        """
        output: list[str] = []
        for row in range(self.height):
            line = self._state[row * self.width : row * self.width + self.width]
            output.append("".join(["#" if element == 1 else "." for element in line]))
        return "\n".join(output)


def part_one(input_lines: list[str]) -> int:

    # Parse the program that the CPU should be executing
    program = Program.from_text(input_lines)

    # Create a device that is running a program
    device = Device(program)

    # Run for 240 ticks (full program) and check the register value at
    # breakpoints
    total = 0
    breaks = [20, 60, 100, 140, 180, 220]
    for tick in range(240):
        device.clock.tick()
        if tick in breaks:
            total += device.cpu.register_x.get_value(tick) * tick

    # Return the sum of the breakpoints
    return total


def part_two(input_lines: list[str]) -> str:

    # Parse the program that the CPU should be executing
    program = Program.from_text(input_lines)

    # Create a device that is running a program
    device = Device(program)

    # Run for 240 ticks (full program) and check the register value at
    # breakpoints
    for _ in range(240):
        device.clock.tick()

    # Render what is on the display as a string
    return device.display.render()


if __name__ == "__main__":

    # Read the input
    with open(Path(__file__).parents[3] / "data/year_2022/day_10.txt", "r") as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Determine the output for part one
    result = part_one(input_lines)
    print("Part one:", result)

    # Determine the output for part two
    result_two = part_two(input_lines)
    print("Part two:\n", result_two)
