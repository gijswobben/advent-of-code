import os
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from random import choice, randint, seed

import browser_cookie3
import click
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pyfiglet import Figlet

# Fix the random seed (for generating christmas ornaments in the banner)
seed(42)

# Determine if the competition is active
NOW = datetime.now()
DEFAULT_YEAR = NOW.year if NOW.month == 12 else NOW.year - 1
DEFAULT_DAY = NOW.day if NOW.month == 12 and NOW.day <= 25 else 1

# Get any cookies from a browser (any browser)
COOKIE_JAR = browser_cookie3.load(domain_name=".adventofcode.com")

# Create the various components of the christmas tree in the banner
BANNER_TREE_BOTTOM = click.style("^", fg="green")
BANNER_TREE_SIDE_LEFT = click.style("/", fg="green")
BANNER_TREE_SIDE_RIGHT = click.style("\\", fg="green")
BANNER_TREE_TOP = click.style("*", fg="yellow", blink=True)
BANNER_TREE_EMPTY = click.style(".", fg="green")
BANNER_TREE_STUMP = click.style("[_]", fg="black")
BANNER_TREE_ORNAMENT = "O"
FESTIVE_COLORS = ["red", "yellow", "blue", "cyan"]


class TreeLayer(ABC):
    """Base class for layers in the christmas tree (banner)."""

    def __init__(self, width: int, max_width: int) -> None:
        self.width = width
        self.max_width = max_width

    @abstractmethod
    def to_string(self) -> str:
        ...


class BranchesLayer(TreeLayer):
    """A layer of branches in the christmas tree."""

    def __init__(self, width: int, max_width: int, n_lines: int = 2):
        super(BranchesLayer, self).__init__(width=width, max_width=max_width)
        self.n_lines = n_lines

    def create_line(self, width: int) -> str:
        ornament_index = randint(0, self.max_width)
        inner = "".join(
            [
                BANNER_TREE_EMPTY
                if index != ornament_index
                else click.style(BANNER_TREE_ORNAMENT, fg=choice(FESTIVE_COLORS))
                for index in range(width)
            ]
        )
        spacing = " " * ((self.max_width - width) // 2)
        return (
            f"{spacing}{BANNER_TREE_SIDE_LEFT}{inner}{BANNER_TREE_SIDE_RIGHT}{spacing}"
        )

    def to_string(self) -> str:
        return "\n".join(
            [
                self.create_line(width)
                for width in range(self.width, (self.width + self.n_lines * 2), 2)
            ]
        )


class TopLayer(TreeLayer):
    """The top ornament of the christmast tree."""

    def create_line(self) -> str:
        spacing = " " * ((self.max_width + 1) // 2)
        return f"{spacing}{BANNER_TREE_TOP}{spacing}"

    def to_string(self) -> str:
        return self.create_line()


class BottomLayer(TreeLayer):
    """The bottom layer of the tree, with the stump."""

    def create_line(self, width: int) -> str:
        spacing = " " * ((self.max_width - 2 - width) // 2)
        bottom = BANNER_TREE_BOTTOM * (((width + 2)) // 2)
        return f"{spacing}{bottom}{BANNER_TREE_STUMP}{bottom}{spacing}"

    def to_string(self) -> str:
        return self.create_line(width=(self.width + 1) // 2)


def get_banner(tree_levels: int = 4) -> str:
    """Create a festive banner for the CLI.

    Args:
        tree_levels (int, optional): Number of levels on the christmas
            tree. Defaults to 4.

    Returns:
        str: A banner as formatted text.
    """
    max_width = 2 * tree_levels + 1

    # Create the tree
    tree_layers: list[TreeLayer] = [
        TopLayer(width=max_width, max_width=max_width),
        *[
            BranchesLayer(width=width, max_width=max_width)
            for width in range(1, 2 * tree_levels, 2)
        ],
        BottomLayer(width=max_width, max_width=max_width),
    ]
    tree_text = "\n".join([layer.to_string() for layer in tree_layers])

    # Center align the tree
    spacing = (80 - max_width) // 2
    tree_text = "\n".join(
        [f"{' ' * spacing}{line}" for line in tree_text.splitlines(keepends=False)]
    )

    # Create the text of the banner
    f = Figlet(font="bell", justify="center")
    text = click.style(f.renderText("Advent of Code"), fg="yellow")

    separator = " " * 20 + click.style("=" * 40, fg="black")
    return tree_text + "\n" + separator + "\n" + text


def download_file(year: int, day: int):
    try:
        os.makedirs(f"data/year_{year}", exist_ok=True)
        r = requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input", cookies=COOKIE_JAR
        )
        r.raise_for_status()
        click.echo(
            click.style(f"Downloaded file for {year} day {day}", fg="green"), err=True
        )
        with open(f"data/year_{year}/day_{day}.txt", "wb") as f:
            f.write(r.content)
    except Exception as e:
        if (
            e.response.text.strip()  # type: ignore
            == "Puzzle inputs differ by user.  Please log in to get your puzzle input."
        ):
            click.echo(
                click.style(
                    "Not authenticated. "
                    "Make sure to log in on a browser before running this command.",
                    fg="red",
                ),
                err=True,
            )
        raise


@click.group()
def cli():

    # Show the banner before each command
    click.echo(get_banner())
    ...


@cli.command()
@click.option(
    "-y",
    "--year",
    default=DEFAULT_YEAR,
    type=click.INT,
    help="Year of the AoC event to download",
    prompt="Select the "
    + click.style("year", fg="green")
    + " for which you'd like to make a challenge",
)
@click.option(
    "-d",
    "--day",
    default=DEFAULT_DAY,
    type=click.INT,
    help="If specified, only download the data for this particular day",
    prompt="Select the "
    + click.style("day", fg="green")
    + " for which you'd like to make a challenge",
)
def new(year: int, day: int):
    """Start a new challenge from a template. This command will create a
    new challenge file, the corresponding test file and will attempt to
    download the data."""

    # Get the paths
    templates_folder = Path(__file__).parents[2] / "templates"
    challenge_filepath = (
        Path(__file__).parents[2] / "src" / "aoc" / f"year_{year}" / f"day_{day}.py"
    )
    test_filepath = (
        Path(__file__).parents[2] / "tests" / f"year_{year}" / f"test_day_{day}.py"
    )

    # Check if the path exists (confirm overwrite if they do)
    if challenge_filepath.exists():
        click.confirm(
            "Challenge file exists, do you want to overwrite?",
            default=False,
            abort=True,
        )
    if test_filepath.exists():
        click.confirm(
            "Test file exists, do you want to overwrite?", default=False, abort=True
        )

    # Get templates folder
    env = Environment(
        loader=FileSystemLoader(templates_folder),
        autoescape=select_autoescape(),
    )

    # Fill and write templates
    challenge_template = env.get_template("challenge_template.py.template")
    with open(challenge_filepath, "w") as f:
        f.write(challenge_template.render(year=year, day=day))
    click.echo(
        click.style(
            f"Written challenge file template to {challenge_filepath.as_posix()}"
        )
    )

    test_template = env.get_template("test_template.py.template")
    with open(test_filepath, "w") as f:
        f.write(test_template.render(year=year, day=day))
    click.echo(
        click.style(f"Written test file template to {challenge_filepath.as_posix()}")
    )

    # Download the dataset for this challenge (if it exists)
    try:
        download_file(year, day)
    except Exception:
        click.echo(click.style("Unable to download file", fg="red"), err=True)


@cli.command()
@click.option(
    "-y",
    "--year",
    default=None,
    type=click.INT,
    help="Year of the AoC event to download",
)
@click.option(
    "-d",
    "--day",
    default=None,
    type=click.INT,
    help="If specified, only download the data for this particular day",
)
def download(year: int | None, day: int | None = None):
    """Download data files from Avent of Code."""

    # Download only a single day
    if day is not None and year is not None:
        try:
            download_file(year, day)
        except Exception:
            click.echo(click.style("Unable to download file", fg="red"), err=True)

    # Download all days for a particular year
    elif day is None and year is not None:
        for day in range(1, 26):
            try:
                download_file(year, day)
            except Exception:
                break

    # Download all (2015 was the first year)
    else:
        for year in range(2015, DEFAULT_YEAR + 1):
            for day in range(1, 26):
                try:
                    download_file(year, day)
                except Exception:
                    break


if __name__ == "__main__":
    cli()
