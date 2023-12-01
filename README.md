![Unittests](https://github.com/gijswobben/advent-of-code/actions/workflows/tests.yaml/badge.svg) ![Python version](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python&logoColor=white&label=Python) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Advent of code

This repository contains my solutions to the [Advent of code challenge](https://adventofcode.com). All the challenges, data files and information about the Advent of code can be found on their website.

I will approach this challenge by using Python, creating 1 script per "day" of the challenge. I will first write a test using the example in the challenge and when the test passes I'll use the created function to generate the answer for the challenge.

## Usage

To use this repostory and run the code, make sure you have a valid installation of Python (3.11). This project uses [Poetry](https://python-poetry.org/) to manage dependencies. Use the following command to install all dependencies:

```shell
$ poetry install
```

## Starting a new challenge

To start a new challenge, run the following command:

```shell
$ poetry run aoc new
```

This command will prompt for the year and day that you want to participate in. After that it will create a new test file and a new script file in the corresponding year and day folder. This command will also download the data file for the challenge and place it in the `data` folder.

## Downloading data

You can run also download the data files manually with the `poetry run aoc download` command (available after installing this package). This will download all available data files for a particular year, day or all years and days (since 2015).

## Testing

`pytest` is used as a testing framework and can be used to test an individual challenge or all challenges with these commands:

```shell
# All challenges
$ poetry run pytest

# All challenges for a particular year
$ poetry run pytest tests/year_2023/test_day_*.py

# Individual challenge
$ poetry run pytest tests/year_2023/test_day_1.py
```

To get the final output for a challenge, the corresponding file can be run using Python:

```shell
$ poetry run python src/aoc/year_2023/day_1.py
```

## Development environment

Personal recommendation: Use [`pyenv`](https://github.com/pyenv/pyenv) to install Python, [`pyenv virtualenv`](https://github.com/pyenv/pyenv-virtualenv) to create an environment and [`poetry`](https://python-poetry.org/) to install and manage dependencies.

## Full walkthrough

```shell
# Install Python and make it the global Python
$ pyenv install 3.11.5
$ pyenv global 3.11.5

# Install Poetry
$ curl -sSL https://install.python-poetry.org | python -

# Set up and activate a new virtual environment
$ pyenv virtualenv 3.11.5 advent-of-code
$ pyenv local advent-of-code

# Install package
$ poetry install --with dev

# Start a new challenge
$ poetry run aoc new
# ...
# Select the year for which you'd like to make a challenge [2023]: 2023
# Select the day for which you'd like to make a challenge [1]: 1
# ...

# Update the tests to match the example in the challenge
# Update the code to pass the tests

# Run tests
$ poetry run pytest tests/year_2023/test_day_1.py

# Get results
$ poetry run python src/aoc/year_2023/day_1.py

# Submit the results to the Advent of code website
```
