"""Solution for Advent of Code day 15."""
import heapq
from pathlib import Path
import doctest
import click


def read_risk_level(filename: Path) -> dict:
    """Read the risk level of the cave

    Args:
        filename (Path): path to the input file.

    Returns:
        dict:   risk level matrix

    Examples:
        >>> x = [print(x) for x in read_risk_level(Path("test/day_15.data"))]
        [1, 1, 6, 3, 7, 5, 1, 7, 4, 2]
        [1, 3, 8, 1, 3, 7, 3, 6, 7, 2]
        [2, 1, 3, 6, 5, 1, 1, 3, 2, 8]
        [3, 6, 9, 4, 9, 3, 1, 5, 6, 9]
        [7, 4, 6, 3, 4, 1, 7, 1, 1, 1]
        [1, 3, 1, 9, 1, 2, 8, 1, 3, 7]
        [1, 3, 5, 9, 9, 1, 2, 4, 2, 1]
        [3, 1, 2, 5, 4, 2, 1, 6, 3, 9]
        [1, 2, 9, 3, 1, 3, 8, 5, 2, 1]
        [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]
    """
    risk_levels = []
    with filename.open("r") as file:
        for line in file:
            risk_levels.append([int(x) for x in line.strip()])
    return risk_levels


def find_lowest_risk_level(risk_level: dict, repetitions: int) -> int:
    """Find the lowest risk level through the caves

    Args:
        risk_level (dict): risk level matrix
        repetitions (int): how often the risk level repeats

    Returns:
        int: lowest risk level through the cave

    Examples:
        >>> find_lowest_risk_level([[1,5,6],[4,2,8],[5,4,9]],1)
        19
        >>> find_lowest_risk_level([[1,5,6],[4,2,8],[5,4,9]],10)
        198
    """
    num_rows = len(risk_level)
    num_cols = len(risk_level[0])
    detlta_row = [-1, 0, 1, 0]
    delt_col = [0, 1, 0, -1]

    cost_map = [
        [None for _ in range(repetitions * num_cols)]
        for _ in range(repetitions * num_rows)
    ]
    positions = [(0, 0, 0)]
    while positions:
        (dist, row, col) = heapq.heappop(positions)
        if (
            row < 0
            or row >= repetitions * num_rows
            or col < 0
            or col >= repetitions * num_cols
        ):
            continue

        val = (
            risk_level[row % num_rows][col % num_cols]
            + (row // num_rows)
            + (col // num_cols)
        )
        while val > 9:
            val -= 9
        rc_cost = dist + val

        if cost_map[row][col] is None or rc_cost < cost_map[row][col]:
            cost_map[row][col] = rc_cost
        else:
            continue
        if row == repetitions * num_rows - 1 and col == repetitions * num_cols - 1:
            break

        for delta in range(4):
            neighbour_row = row + detlta_row[delta]
            neighbour_col = col + delt_col[delta]
            heapq.heappush(
                positions, (cost_map[row][col], neighbour_row, neighbour_col)
            )
    return (
        cost_map[repetitions * num_rows - 1][repetitions * num_cols - 1]
        - risk_level[0][0]
    )


@click.group()
def main():
    """CLI for the solution of day 15

    Advent of code 2021 (https://adventofcode.com/2021/day/15)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test/day_15.data"),
)
def part_1(filename: Path):
    """Part one of day 15. (1 x input)"""
    risk_level = find_lowest_risk_level(read_risk_level(filename), 1)
    print(f"The lowest possible risk level through the cave is {risk_level}")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test/day_15.data"),
)
def part_2(filename: Path):
    """Part two of day 15. (5 x input)"""
    risk_level = find_lowest_risk_level(read_risk_level(filename), 5)
    print(f"The lowest possible risk level through the cave is {risk_level}")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
