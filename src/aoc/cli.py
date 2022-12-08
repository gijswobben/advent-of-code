import os
from datetime import datetime
from pathlib import Path

import browser_cookie3
import click
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

NOW = datetime.now()
DEFAULT_YEAR = NOW.year if NOW.month == 12 else NOW.year - 1

# Get any cookies from a browser (any browser)
COOKIE_JAR = browser_cookie3.load(domain_name=".adventofcode.com")


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
    ...


@cli.command()
@click.option(
    "-y",
    "--year",
    default=DEFAULT_YEAR,
    type=click.INT,
    help="Year of the AoC event to download",
    prompt=True,
)
@click.option(
    "-d",
    "--day",
    default=1,
    type=click.INT,
    help="If specified, only download the data for this particular day",
    prompt=True,
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
            f"Challenge file exists, do you want to overwrite?",
            default=False,
            abort=True,
        )
    if test_filepath.exists():
        click.confirm(
            f"Test file exists, do you want to overwrite?", default=False, abort=True
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

    # Get any cookies from a browser (any browser)
    cj = browser_cookie3.load(domain_name=".adventofcode.com")

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
