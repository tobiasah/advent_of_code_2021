"""Solution for Advent of Code day 13."""
from pathlib import Path
import re
import doctest
import click


def extract_integers(line: str) -> list[int]:
    """extract integers fromstring.

    Args:
        line (str): input line

    Returns:
        list[int]: found integers

    Examples:
        >>> extract_integers("10,4")
        [10, 4]
        >>> extract_integers("x=408z")
        [408]
        >>> extract_integers("fold along x=0")
        [0]
    """
    return list(map(int, re.findall(r"\d+", line)))


def read_instruction(filename: Path) -> tuple[list[list[int]], list[str]]:
    """Read the points and instructions form a file.

    Args:
        filename (Path): path to the input file.

    Returns:
        list[list[int]] points
        list[str] instructions

    Examples:
        >>> read_instruction(Path("test_data/day_13.data"))[0][0]
        [6, 10]
        >>> read_instruction(Path("test_data/day_13.data"))[1][0]
        'fold along y=7'
    """
    with filename.open("r") as file:
        points, instructions = file.read().split("\n\n")
    points = [extract_integers(line) for line in points.split("\n")]
    instructions = instructions.strip().split("\n")
    return points, instructions


def fold(points: list[list[int]], instructions: list[str]) -> list[list[int]]:
    """Folds a plane with points according to the instructions.

    Args:
        points (list[list[int]]): points on a plane
        instructions (list[str]): instruction where the plane should be folded

    Returns:
        list[list[int]]: resulting points

    Examples:
        >>> fold([[1,0],[-1,0]], ["fold along x=0"])
        [(-1, 0), (-1, 0)]
        >>> fold([[1,6],[-1,-4]], ["fold along y=3"])
        [(1, 0), (-1, -4)]
    """
    for instruction in instructions:
        pos = extract_integers(instruction)[0]
        if "x" in instruction:
            points = [(x if x < pos else pos - (x - pos), y) for x, y in points]
        else:
            points = [(x, y if y < pos else pos - (y - pos)) for x, y in points]
    return points


@click.group()
def main():
    """CLI for the solution of day 13

    Advent of code 2021 (https://adventofcode.com/2021/day/13)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_13.data"),
)
def part_1(filename: Path):
    """Part one of day 13. (num of points after first instruction)"""
    points, instructions = read_instruction(filename)
    points = fold(points, [instructions[0]])

    print(f"After once instruction there are {len(set(points))} dots visible.")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_13.data"),
)
def part_2(filename: Path):
    """Part two of day 13. (print code)"""
    points, instructions = read_instruction(filename)
    points = fold(points, instructions)

    num_columns = max([*zip(*points)][0]) + 1
    num_rows = max([*zip(*points)][1]) + 1
    grid = [[0] * num_columns for i in range(num_rows)]
    for x, y in points:
        grid[y][x] = 1
    for row in grid:
        print("".join(" #"[col] for col in row))


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
