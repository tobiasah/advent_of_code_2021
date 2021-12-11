"""Solution for Advent of Code day 10."""
from pathlib import Path
from collections import deque
import doctest
import click
import math
from typing import Union

def analyse_lines(filename: Path) -> tuple[bool, Union[str,list]]:
    """Analyse the lines of a file

    if the line is corrupt (closing brackets does not match opening) it
    yields the wrong charakter. Else it yields the missing closing brackets
    to finish the line.

    Args:
        filename (Path): path to the input file.

    Yields:
        bool: Flag if the line is broken or not.
        Union[str,list]: the broken char or the missing closing brackets to
                         finish the line.

    Examples:
        >>> next(analyse_lines(Path("test_data/day_10.data")))
        (False, ['}', '}', ']', ']', ')', '}', ')', ']'])
        >>> x = [print(i) for i in analyse_lines(Path("test_data/day_10.data"))]
        (False, ['}', '}', ']', ']', ')', '}', ')', ']'])
        (False, [')', '}', '>', ']', '}', ')'])
        (True, '}')
        (False, ['}', '}', '>', '}', '>', ')', ')', ')', ')'])
        (True, ')')
        (True, ']')
        (False, [']', ']', '}', '}', ']', '}', ']', '}', '>'])
        (True, ')')
        (True, '>')
        (False, [']', ')', '}', '>'])
    """
    opener = ["(", "[", "{", "<"]
    closer = [")", "]", "}", ">"]
    with filename.open("r") as file:
        for line in file:
            char_queue = deque()
            broken = False
            for char in line.strip():
                try:
                    char_queue.append(opener.index(char))
                except ValueError:
                    if char_queue.pop() != closer.index(char):
                        broken = True
                        yield broken, char
                        break
            if not broken:
                yield broken, [closer[item] for item in reversed(char_queue)]


@click.group()
def main():
    """CLI for the solution of day 10

    Advent of code 2021 (https://adventofcode.com/2021/day/10)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_10.data"),
)
def part_1(filename: Path):
    """Part one of day 10. (score broken lines)"""
    score = {")": 3, "]": 57, "}": 1197, ">": 25137}
    result = sum([score[char] for broken, char in analyse_lines(filename) if broken])
    print(f"The score of all broken lines is : {result}")

@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_10.data"),
)
def part_2(filename: Path):
    """Part two of day nitenne. (middle score of incomplete lines)"""
    score = {")": 1, "]": 2, "}": 3, ">": 4}
    incomplete_lines = [line for broken, line in analyse_lines(filename) if not broken]
    scores = []
    for line in incomplete_lines:
        scores.append(sum([5 ** i * score[item] for i, item in enumerate(reversed(line))]))
    scores.sort()
    result = scores[math.floor(len(scores)/2)]
    print(f"The middle score of incomplete lines is: {result}")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
