"""Solution for Advent of Code day 7."""
from functools import lru_cache
import sys
import doctest
from typing import Callable
from pathlib import Path
import click


@lru_cache(maxsize=None)
def cost_function_part2(num_steps: int) -> int:
    """Recursive cost function for the second part.

    The first step costs 1, the second step costs 2, the third step costs 3,
    and so on.

    Args:
        num_steps (int): Number of Steps

    Returns:
        (int) cost

    Examples:
        >>> cost_function_part2(0)
        0
        >>> cost_function_part2(1)
        1
        >>> cost_function_part2(2)
        3
        >>> cost_function_part2(1000)
        500500
    """
    return cost_function_part2(num_steps - 1) + num_steps if num_steps > 0 else 0


def optimal_position(positions: list, cost_function: Callable):
    """Calculate the optimal position which minimises the cost.

    Warning: This function assumes that there is no local minimum

    Args:
        positions (list): list of input points
        cost_function (Callable): cost function taking the distance as input

    Returns:
        (int) Cost of the minimum

    Examples:
        >>> optimal_position([0,1,2],lambda distance: distance)
        2
        >>> optimal_position([0,1,2],cost_function_part2)
        2
        >>> optimal_position([16,1,2,0,4,2,7,1,2,14],lambda distance: distance)
        37
        >>> optimal_position([16,1,2,0,4,2,7,1,2,14],cost_function_part2)
        168

    """
    minimum = sum([cost_function(abs(pos)) for pos in positions])
    for i in range(1, max(positions)):
        new = sum([cost_function(abs(pos - i)) for pos in positions])
        if new < minimum:
            minimum = new
        else:
            break
    return minimum


@click.group()
def main():
    """CLI for the solution of day 7

    Advent of code 2021 (https://adventofcode.com/2021/day/7)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_7.data"),
)
def part_1(filename: Path):
    """Part one of day seven. (linear cost)"""
    optimum = optimal_position(
        [int(item) for item in filename.open("r").read().split(",")],
        lambda distance: distance,
    )
    print(f"Minimal cost is: {optimum}")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_7.data"),
)
def part_2(filename: Path):
    """Part two of day four. (find loosing board)"""
    old_depth = sys.getrecursionlimit()
    sys.setrecursionlimit(10000)
    optimum = optimal_position(
        [int(item) for item in filename.open("r").read().split(",")],
        cost_function_part2,
    )
    sys.setrecursionlimit(old_depth)
    print(f"Minimal cost is: {optimum}")


@main.command()
def test():
    """run doctest."""
    old_depth = sys.getrecursionlimit()
    sys.setrecursionlimit(10000)
    print(doctest.testmod())
    sys.setrecursionlimit(old_depth)


if __name__ == "__main__":
    main()
