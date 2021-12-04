"""Solution for Advent of Code day 3."""
from pathlib import Path
import doctest
from typing import Iterable, Iterator
import click


def read_as_int_list(filename: Path) -> Iterator[list[int]]:
    """Read file as interger list.

    Read file line by line and convert each line into a list of intergers.

    Args:
        filename (Path): path to the input file.

    Yields:
        int: The next line as list of intergers.

    Examples:
        >>> next(read_as_int_list(Path("test_data/day_3.data")))
        [0, 0, 1, 0, 0]
    """
    with filename.open("r") as file:
        for line in file:
            data = [int(char) for char in line.strip()]
            yield data


def bitwise_most_common_bit(input_iter: Iterable) -> list[int]:
    """Calculate the most common bit for each position.

    The elements are binaries reperesentet in a list of intergers.
    Each element must have the same length.

    WARNING: The input does not undergo a sanity check.

    Args:
        input_iter (Iterable): Iterable with lists of intergers representing a binary

    Returns:
        (list[int]) Most common bit for each position. If both 0

    Examples:
        >>> int_list_to_bin([0, 1])
        1
        >>> int_list_to_bin([1, 0, 1, 0, 1, 0, 1])
        85
        >>> int_list_to_bin([2, 5, 7])
        25
        >>> int_list_to_bin([])
        0
    """
    counter = next(input_iter)
    num_lines = 1
    for element in input_iter:
        counter = [x + y for x, y in zip(counter, element)]
        num_lines = num_lines + 1
    return [int(x >= num_lines / 2) for x in counter]


def int_list_to_bin(int_list: list[int]) -> int:
    """Interpret a list of integers as a binary.

    WARNING: The input does not undergo a sanity check.

    Args:
        int_list (list[int]): List of integer representing a binary.

    Returns:
        (int) Binary as integer.

    Examples:
        >>> int_list_to_bin([0])
        0
        >>> int_list_to_bin([0, 1])
        1
        >>> int_list_to_bin([1, 0, 1, 0, 1, 0, 1])
        85
        >>> int_list_to_bin([2, 5, 7])
        25
        >>> int_list_to_bin([])
        0
    """
    return sum(c << i for i, c in enumerate(reversed(int_list)))


@click.group()
def main():
    """CLI for the solution of day 3

    Advent of code 2021 (https://adventofcode.com/2021/day/3)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_3.data"),
)
def part_1(filename: Path):
    """Part one of day three. (power consumption)"""
    gamma_rate = bitwise_most_common_bit(read_as_int_list(filename))
    epsilon_rate = [int(not x) for x in gamma_rate]
    gamma_rate = int_list_to_bin(gamma_rate)
    epsilon_rate = int_list_to_bin(epsilon_rate)
    print(f"power consumption of submarine: {gamma_rate * epsilon_rate}")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_3.data"),
)
def part_2(filename: Path):
    """Part two of day three. (life support rating)"""
    oxy_remainders = list(read_as_int_list(filename))
    co2_remainders = oxy_remainders
    counter = 0
    while len(oxy_remainders) > 1:
        criteria = bitwise_most_common_bit(iter(oxy_remainders))[counter]
        oxy_remainders = [
            element for element in oxy_remainders if element[counter] == criteria
        ]
        counter = counter + 1
    counter = 0
    while len(co2_remainders) > 1:
        criteria = bitwise_most_common_bit(iter(co2_remainders))[counter]
        co2_remainders = [
            element for element in co2_remainders if element[counter] != criteria
        ]
        counter = counter + 1

    oxygen_generator_rating = int_list_to_bin(oxy_remainders[0])
    co2_scrubber_rating = int_list_to_bin(co2_remainders[0])

    print(
        f"life support rating of the submarine: {oxygen_generator_rating * co2_scrubber_rating}"
    )


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
