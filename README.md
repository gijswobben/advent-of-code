![Unittests](https://github.com/gijswobben/advent-of-code-2022/actions/workflows/tests.yaml/badge.svg) ![Python version](https://img.shields.io/github/pipenv/locked/python-version/gijswobben/advent-of-code-2022?label=Python&logo=Python&logoColor=white) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Advent of code - 2022
This repository contains my solutions to the [Advent of code challenge 2022](https://adventofcode.com/2022). All the challenges, data files and information about the Advent of code can be found on their website.

I will approach this challenge by using Python, creating 1 script per "day" of the challenge. I will first write a test using the example in the challenge and when the test passes I'll use the created function to generate the answer for the challenge.

## Usage
Before running the code, make sure to download the data for the challenges. This can be done by logging in on the the Advent of code website and saving the content of the input file, e.g. https://adventofcode.com/2022/day/1/input. Make sure to store the file in the data folder of this project and use `data/day_{DAY_NUMBER}.txt` as the filename (example: `data/day_1.txt`, `data/day_2.txt`, ...). Note: The data files are user specific, you will have a different input file and answer!

To use this repostory and run the code, make sure you have a valid installation of Python (3.10). This project uses `pipenv` to manage dependencies. The following commands will install `pipenv` and the project dependencies.

```shell
$ python -m pip install "pipenv==2022.11.30"
$ pipenv install --dev
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
