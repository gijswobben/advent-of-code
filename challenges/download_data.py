from datetime import datetime

import browser_cookie3
import click
import requests

cj = browser_cookie3.load(domain_name=".adventofcode.com")

NOW = datetime.now()
DEFAULT_YEAR = NOW.year if NOW.month == 12 else NOW.year - 1


def download_file(year: int, day: int):
    try:
        r = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cj)
        r.raise_for_status()
        click.echo(click.style(f"Downloaded file for day {day}", fg="green"), err=True)
        with open(f"data/day_{day}.txt", "wb") as f:
            f.write(r.content)
    except Exception as e:
        if (
            e.response.text.strip()  # type: ignore
            == "Puzzle inputs differ by user.  Please log in to get your puzzle input."
        ):
            click.echo(
                click.style(
                    "Not authenticated. Make sure to log in on a browser before running this command.",
                    fg="red",
                ),
                err=True,
            )
        raise


@click.command()
@click.option(
    "-y",
    "--year",
    default=DEFAULT_YEAR,
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
def download_datafiles(year: int = 2022, day: int | None = None):
    """Commandline tool to automatically download all the data files
    from Advent of Code (aoc). This tools downloads all the available
    datafiles for the most recent AoC event."""

    # Download only a single day
    if day is not None:
        try:
            download_file(year, day)
        except Exception:
            click.echo(click.style("Unable to download file", fg="red"), err=True)

    # Download all days for a particular year
    else:
        for day in range(1, 26):
            try:
                download_file(year, day)
            except Exception:
                break


if __name__ == "__main__":
    download_datafiles()
