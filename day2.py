"""Solution for Advent of Code day 2."""
from pathlib import Path
from typing import Iterator
import doctest
import click

def course_updates(filename: Path) -> Iterator[int]:
    """Generator thats yield each line from a file as a number.

    Args:
        filename (Path): path to the input file.

    Yields:
        int: The next number from the file.

    Examples:
        >>> next(course_updates(Path("test_data/day_2.data")))
        (5, 0)
        >>> [i for i in course_updates(Path("test_data/day_2.data"))]
        [(5, 0), (0, 5), (8, 0), (0, -3), (0, 8), (2, 0)]
    """
    with filename.open("r") as file:
        for line in file:
            if line.startswith("forward"):
                yield int(line.strip()[-1]), 0
            elif line.startswith("down"):
                yield 0, int(line.strip()[-1])
            else:
                yield 0, -int(line.strip()[-1])


@click.group()
def main():
    """CLI for the solution of day 2

    Advent of code 2021 (https://adventofcode.com/2021/day/2)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_2.data"),
)
def part_1(filename: Path):
    """Part one of day two. (position)"""
    position = (0, 0)
    for horizontal, vertical in course_updates(filename):
        position = tuple(sum(x) for x in zip(position, (horizontal, vertical)))
    print(position[0] * position[1])


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_2.data"),
)
def part_2(filename: Path):
    """Part two of day two. (position & aim)"""
    position = (0, 0)
    aim = 0
    for pos_delta, aim_delta in course_updates(filename):
        aim = aim + aim_delta
        position = tuple(sum(x) for x in zip(position, (pos_delta, pos_delta * aim)))
    print(position[0] * position[1])


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
