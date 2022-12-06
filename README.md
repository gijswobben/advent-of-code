![Unittests](https://github.com/gijswobben/advent-of-code-2022/actions/workflows/tests.yaml/badge.svg) ![Python version](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python&logoColor=white&label=Python) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Advent of code - 2022
This repository contains my solutions to the [Advent of code challenge 2022](https://adventofcode.com/2022). All the challenges, data files and information about the Advent of code can be found on their website.

I will approach this challenge by using Python, creating 1 script per "day" of the challenge. I will first write a test using the example in the challenge and when the test passes I'll use the created function to generate the answer for the challenge.

## Usage
Before running the code, make sure to download the data for the challenges. This can be done by logging in on the the Advent of code website and saving the content of the input file, e.g. https://adventofcode.com/2022/day/1/input. Make sure to store the file in the data folder of this project and use `data/day_{DAY_NUMBER}.txt` as the filename (example: `data/day_1.txt`, `data/day_2.txt`, ...). Note: The data files are user specific, you will have a different input file and answer!

Alternatively you can run the `aoc` command (available after installing this package) to download all available data files.

To use this repostory and run the code, make sure you have a valid installation of Python (3.10). This project uses [Poetry](https://python-poetry.org/) to manage dependencies. Use the following command to install all dependencies:

```shell
$ poetry install
```

`pytest` is used as a testing framework and can be used to test an individual challenge or all challenges with these commands:

```shell
# All challenges
$ pytest challenges/day_*.py

# Individual challenge
$ pytest challenges/day_1.py
```

To get hte final output for a challenge, the corresponding file can be run using Python:

```shell
$ python challenges/day_1.py
```

Personal recommendation: Use [`pyenv`](https://github.com/pyenv/pyenv) to install Python, [`pyenv virtualenv`](https://github.com/pyenv/pyenv-virtualenv) to create an environment and [`poetry`](https://python-poetry.org/) to install and manage dependencies.

Full walkthrough (example for MacOs):

```shell
# Install Python and make it the global Python
$ pyenv install 3.10.8
$ pyenv global 3.10.8

# Install Poetry
$ curl -sSL https://install.python-poetry.org | python -

# Install package
$ poetry install --with dev

# Run tests
$ poetry run pytest

# Download all data files
$ poetry run aoc

# Get results for day 1
$ poetry run python challenges/day_1.py
```
