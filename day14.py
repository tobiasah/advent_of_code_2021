"""Solution for Advent of Code day 14."""
from collections import Counter
import doctest
from pathlib import Path
import click


def read_polymer(filename: Path) -> tuple[dict, str]:
    """Read polymer structure information from a file

    The polymer is represented by a dict of rules and a polymer structer.

    Args:
        filename (Path): path to the input file.

    Returns:
        dict:   rules
        str:    initial polymer structure

    Examples:
        >>> read_polymer(Path("test_data/day_14.data"))[0]['CH']
        'B'
        >>> read_polymer(Path("test_data/day_14.data"))[1]
        'NNCB'
    """
    with filename.open("r") as file:
        poly_template, rules_raw = file.read().split("\n\n")
    rules = {}
    for line in rules_raw.strip().split("\n"):
        start, end = line.strip().split(" -> ")
        rules[start] = end

    return rules, poly_template


def breakdown_structure(connection_counter: Counter, rules: dict) -> Counter:
    """breaksdown the polymer structure and add new elements

    Args:
        connection_counter (Counter): Initial count of each connection
        rules (dict): Rules how to break down each connection

    Returns:
        Counter: new polymer structure represented by the number for each pairs

    Examples:
        >>> breakdown_structure(Counter(AB = 1), {"AB":"C"})
        Counter({'AC': 1, 'CB': 1})
        >>> breakdown_structure(Counter(AB = 1, BC = 4), {"AB":"C", "BC":"A"})
        Counter({'AC': 5, 'BA': 4, 'CB': 1})
    """
    new_counter = Counter()
    for poly_pair in connection_counter:
        new_counter[poly_pair[0] + rules[poly_pair]] += connection_counter[poly_pair]
        new_counter[rules[poly_pair] + poly_pair[1]] += connection_counter[poly_pair]
    return new_counter


def get_puzzel_answer(connection_counter, poly_template) -> int:
    """Count each pair and calculate the puzzel result

    What do you get if you take the quantity of the most common element and
    subtract the quantity of the least common element?

    Args:
        connection_counter (Counter): Initial count of each connection
        poly_template (str): initial polymer structur

    Returns:
        int:    puzzel result

    Examples:
        >>> get_puzzel_answer(Counter({'AC': 5, 'BA': 4, 'CB': 1}), "ABC")
        3
    """
    char_counter = Counter()
    for k in connection_counter:
        char_counter[k[0]] += connection_counter[k]
    # The last charakter of the polymer needs to be counted as well
    char_counter[poly_template[-1]] += 1
    return max(char_counter.values()) - min(char_counter.values())


@click.group()
def main():
    """CLI for the solution of day 14

    Advent of code 2021 (https://adventofcode.com/2021/day/14)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_14.data"),
)
def part_1(filename: Path):
    """Part one of day 14. (10 steps)"""
    rules, poly_template = read_polymer(filename)
    # Keep track of how often each pair of letters occures in the polymer
    connection_counter = Counter()
    for i in range(len(poly_template) - 1):
        connection_counter[poly_template[i] + poly_template[i + 1]] += 1

    for _ in range(10):
        connection_counter = breakdown_structure(connection_counter, rules)
    print(
        "quantity of the most common element - quantity of the least "
        f"common element: {get_puzzel_answer(connection_counter,poly_template)}"
    )


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_14.data"),
)
def part_2(filename: Path):
    """Part two of day 14. (40 steps)"""
    rules, poly_template = read_polymer(filename)
    # Keep track of how often each pair of letters occures in the polymer
    connection_counter = Counter()
    for i in range(len(poly_template) - 1):
        connection_counter[poly_template[i] + poly_template[i + 1]] += 1

    for _ in range(40):
        connection_counter = breakdown_structure(connection_counter, rules)
    print(
        "quantity of the most common element - quantity of the least "
        f"common element: {get_puzzel_answer(connection_counter,poly_template)}"
    )


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
