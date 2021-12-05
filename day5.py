"""Solution for Advent of Code day 5."""
from pathlib import Path
import doctest
from typing import Iterable, Iterator
import numpy as np
import click


def read_as_2d_line(filename: Path) -> Iterator[tuple[int, int, int, int, bool]]:
    """read lines from file and convert them 2D lines

    The lines are specified through start and end point that are seperated
    with ' -> '. Each point consists of its 2D coordinates seperated by a comma.

    Args:
        filename (Path): path to the input file.

    Yields:
        (int): x_1 (x coordinate of the start point)
        (int): x_2 (x coordinate of the end point)
        (int): y_1 (y coordinate of the start point)
        (int): y_2 (y coordinate of the end point)
        (bool): Flag if the line is a diagonal (True)
                or horizontal/vertical line (False)

    Examples:
        >>> next(read_as_2d_line(Path("test_data/day_5.data")))
        (0, 5, 9, 9, False)
    """
    with filename.open("r") as file:
        for line in file:
            start_pos, stop_pos = line.strip().split(" -> ")
            x_1, y_1 = (int(cor) for cor in start_pos.split(","))
            x_2, y_2 = (int(cor) for cor in stop_pos.split(","))

            if x_1 == x_2 or y_1 == y_2:
                y_1, y_2 = (y_2, y_1) if y_1 > y_2 else (y_1, y_2)
                x_1, x_2 = (x_2, x_1) if x_1 > x_2 else (x_1, x_2)
                yield x_1, x_2, y_1, y_2, False
            elif abs(x_1 - x_2) == abs(y_1 - y_2):
                yield x_1, x_2, y_1, y_2, True


def calc_points_overlaping(
    lines: Iterable[tuple[int, int, int, int, bool]],
    use_diagonals: bool = True,
    field_size: int = 10,
) -> int:
    """Calculates the number of overlapping points from a list of lines.


    Args:
        lines (Iterable[tuple[int, int, int, int, bool]]): Iterable with lines
            defined as tuple. A line consists of start and end point and a Flag
            if the line is diagonal or horizontal/vertical. The expected order
            in the tuple is x-pos start, x-pos stop, y-pos start, y-pos stop, Flag.

    Returns:
        (int) number of overlaping points.

    Examples:
        >>> calc_points_overlaping([(0, 5, 9, 9, False)])
        0
        >>> calc_points_overlaping([(0, 5, 9, 9, False),(2, 3, 9, 9, False)])
        2
        >>> calc_points_overlaping([(0, 5, 9, 9, False),(0, 0, 9, 5, False)])
        0
        >>> calc_points_overlaping([(0, 5, 9, 9, False),(0, 4, 9, 5, True)])
        1
    """
    vent_diagramm = np.zeros(shape=(field_size, field_size), dtype=np.uint8)

    for x_1, x_2, y_1, y_2, is_diag in lines:
        if use_diagonals and is_diag:
            delta_x = 1 if x_2 > x_1 else -1
            delta_y = 1 if y_2 > y_1 else -1
            for i in range(abs(x_2 - x_1) + 1):
                vent_diagramm[x_1 + (delta_x * i), y_1 + (delta_y * i)] += 1
        elif not is_diag:
            vent_diagramm[x_1 : x_2 + 1, y_1 : y_2 + 1] += 1

    return len(np.where(vent_diagramm >= 2)[0])


@click.group()
def main():
    """CLI for the solution of day 5

    Advent of code 2021 (https://adventofcode.com/2021/day/5)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_5.data"),
)
@click.argument(
    "max-size",
    required=False,
    type=int,
    default=10,
)
def part_1(filename: Path, max_size: int):
    """Part one of day five. (field with horizontals and verticals)"""

    overlaping_count = calc_points_overlaping(
        read_as_2d_line(filename), use_diagonals=False, field_size=max_size
    )
    print(
        "Considering horizontal,vertical and diagonal lines results in "
        f"{overlaping_count} overlaping points."
    )


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_5.data"),
)
@click.argument(
    "max-size",
    required=False,
    type=int,
    default=10,
)
def part_2(filename: Path, max_size: int):
    """Part two of day five. (field with horizontals, verticals and diagonals)"""

    overlaping_count = calc_points_overlaping(
        read_as_2d_line(filename), use_diagonals=True, field_size=max_size
    )
    print(
        "Considering only horizontal/vertical lines results in "
        f"{overlaping_count} overlaping points."
    )


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
