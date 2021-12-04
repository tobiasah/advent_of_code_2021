"""Solution for Advent of Code day 1."""

import collections
from pathlib import Path
from typing import Iterable, Iterator
import doctest
import click


def count_increases(iterable: Iterable[int]) -> int:
    """Counts the number of increases of a number.

    An increase is given if a number is higher than its predecessor.

    Args:
        iterable (Iterable): iteratable object of type int

    Returns:
        int: number of increases.

    Examples:
        >>> count_increases([199,200,208,210,200,207,240,269,260,263])
        7
        >>> count_increases(range(10))
        9
        >>> count_increases([])
        0
    """
    last_number = None
    increase_count = 0
    for number in iterable:
        if last_number is not None and last_number < number:
            increase_count = increase_count + 1
        last_number = number
    return increase_count


def number_from_line(filename: Path) -> Iterator[int]:
    """Generator thats yield each line from a file as a number.

    Args:
        filename (Path): path to the input file.

    Yields:
        int: The next number from the file.

    Examples:
        >>> next(number_from_line(Path("test_data/day_1.data")))
        199
        >>> [i for i in number_from_line(Path("test_data/day_1.data"))]
        [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    """
    with filename.open("r") as file:
        for line in file:
            yield int(line.strip())


def number_from_window(filename: Path, window_size: int) -> Iterator[int]:
    """Generator thats yield a sliding window line from a file as a number.

    The number of lines in the file must be greater or equal to the window_size.

    Args:
        filename (Path): path to the input file.
        window_size (int): size of the sliding window.

    Yields:
        int: The sum of the next window.

    Examples:
        >>> next(number_from_window(Path("test_data/day_1.data"), 3))
        607
        >>> next(number_from_window(Path("test_data/day_1.data"), 1))
        199
        >>> next(number_from_window(Path("test_data/day_1.data"), 10))
        2256
        >>> next(number_from_window(Path("test_data/day_1.data"), 11))
        Traceback (most recent call last):
        ValueError: invalid literal for int() with base 10: ''
        >>> [i for i in number_from_window(Path("test_data/day_1.data"), 3)]
        [607, 618, 618, 617, 647, 716, 769, 792]
    """
    with filename.open("r") as file:
        circ_queue = collections.deque(maxlen=window_size)
        for _ in range(window_size):
            circ_queue.append(int(file.readline().strip()))
        yield sum(circ_queue)
        line = file.readline()
        while line:
            circ_queue.append(int(line.strip()))
            yield sum(circ_queue)
            line = file.readline()

@click.group()
def main():
    """CLI for the solution of day 1

    Advent of code 2021 (https://adventofcode.com/2021/day/1)
    """

@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_1.data"),
)
@click.option(
    "--window",
    required=False,
    type=int,
    help="Apply sliding window.",
)
def counter(filename:Path, window:int):
    """Part one (without window) and part two (with window) of day one."""
    if window:
        print(
            f"sum (window = {window}): "
            f"{count_increases(number_from_window(filename, window))}"
        )
    else:
        print(f"sum: {count_increases(number_from_line(filename))}")

@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())

if __name__ == '__main__':
    main()
