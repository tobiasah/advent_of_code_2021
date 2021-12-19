"""Solution for Advent of Code day 18."""
import itertools
import math
from functools import reduce
from typing import Union
from pathlib import Path
import doctest
import click


SnailNumber = list[Union[int, "SnailNumber"], Union[int, "SnailNumber"]]


def add_left(number: SnailNumber, element: int) -> SnailNumber:
    """Add element to the first regular number to the left.

    Args:
        number (SnailNumber): snail number
        element (int) element that should be added

    Returns:
        (SnailNumber): resulting snail number

    Examples:
        >>> add_left([1, 7] ,8)
        [9, 7]
        >>> add_left([[1, 7], [9, 6]],8)
        [[9, 7], [9, 6]]
        >>> add_left([9, 7],8)
        [17, 7]
        >>> add_left([9, 7],None)
        [9, 7]
    """
    if element is None:
        return number
    if isinstance(number, int):
        return number + element
    return [add_left(number[0], element), number[1]]


def add_right(number: SnailNumber, element: int) -> SnailNumber:
    """Add element to the first regular number to the right.

    Args:
        number (SnailNumber): snail number
        element (int) element that should be added

    Returns:
        (SnailNumber): resulting snail number

    Examples:
        >>> add_right([1, 7] ,8)
        [1, 15]
        >>> add_right([[1, 7], [9, 6]],8)
        [[1, 7], [9, 14]]
        >>> add_right([9, 7],8)
        [9, 15]
        >>> add_right([9, 7],None)
        [9, 7]
    """
    if element is None:
        return number
    if isinstance(number, int):
        return number + element
    return [number[0], add_right(number[1], element)]


def explode(
    number: SnailNumber, nested_depth: int = 0
) -> tuple[bool, int, SnailNumber, int]:
    """Explodes a pair/snail number if neccessary.

    To explode a pair, the pair's left value is added to the first regular
    number to the left of the exploding pair (if any), and the pair's right
    value is added to the first regular number to the right of the exploding
    pair (if any). Exploding pairs will always consist of two regular numbers.
    Then, the entire exploding pair is replaced with the regular number 0.

    This function is a recurvice function.

    Args:
        number (SnailNumber): Number that should be exploded
        nested_count (int): How deep the number is nested.

    Returns:
        (bool) Flag if number exploded
        (int) left element
        (SnailNumber) resulting number
        (int) right element

    Examples:
        >>> explode([[1, 7] , [3, 5]])
        (False, None, [[1, 7], [3, 5]], None)
        >>> explode([[6,[5,[4,[3,2]]]],1])
        (True, None, [[6, [5, [7, 0]]], 3], None)
        >>> explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
        (True, None, [[3, [2, [8, 0]]], [9, [5, [7, 0]]]], 2)
    """
    if isinstance(number, int):
        return False, None, number, None
    if nested_depth == 4:
        return True, number[0], 0, number[1]
    left_part, right_part = number
    exp, left, left_part, right = explode(left_part, nested_depth + 1)
    if exp:
        return True, left, [left_part, add_left(right_part, right)], None
    exp, left, right_part, right = explode(right_part, nested_depth + 1)
    if exp:
        return True, None, [add_right(left_part, left), right_part], right
    return False, None, number, None


def split(number: SnailNumber) -> tuple[bool, SnailNumber]:
    """Split a number if neccessary.

    To split a regular number, replace it with a pair; the left element of the
    pair should be the regular number divided by two and rounded down, while the
    right element of the pair should be the regular number divided by two and
    rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes
    [6,6], and so on.

    This function is a recurvice function.

    Args:
        number (SnailNumber): Number that should be splitted

    Returns:
        (bool) Flag if number splitted
        (SnailNumber) resulting number

    Examples:
        >>> split([[1, 7] , [3, 5]])
        (False, [[1, 7], [3, 5]])
        >>> split([[[[0,7],4],[15,[0,13]]],[1,1]])
        (True, [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]])
        >>> split([[[[0,7],4],[[7,8],[0,13]]],[1,1]])
        (True, [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]])
    """
    if isinstance(number, int):
        if number >= 10:
            return True, [number // 2, math.ceil(number / 2)]
        return False, number
    left_part, right_part = number
    change, left_part = split(left_part)
    if change:
        return True, [left_part, right_part]
    change, right_part = split(right_part)
    return change, [left_part, right_part]


def add(number_1: SnailNumber, number_2: SnailNumber) -> SnailNumber:
    """Adds two snail numbers.

    Args:
        number_1 (SnailNumber): first number
        number_2 (SnailNumber): second number

    Returns:
        (SnailNumber): resulting number

    Examples:
        >>> add([1,1],[2,2])
        [[1, 1], [2, 2]]
        >>> add([[[[1,1],[2,2]],[3,3]],[4,4]],[5,5])
        [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
    """
    result = [number_1, number_2]
    while True:
        change, _, result, _ = explode(result)
        if change:
            continue
        change, result = split(result)
        if not change:
            break
    return result


def magnitude(number: SnailNumber) -> int:
    """Calculates the magnitude of asnail number

    Args:
        number (SnailNumber): input number

    Returns:
        (int): mangitude

    Examples:
        >>> magnitude([[1, 1], [2, 2]])
        35
        >>> magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
        1384
    """
    if isinstance(number, int):
        return number
    return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


@click.group()
def main():
    """CLI for the solution of day 18

    Advent of code 2021 (https://adventofcode.com/2021/day/18)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_18.data"),
)
def part_1(filename: Path):
    """Part one of day 18. (magnitute)"""
    with filename.open("r") as file:
        lines = list(map(eval, file.read().splitlines()))
    print(f"Magnitude of the result is: {magnitude(reduce(add, lines))}")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_18.data"),
)
def part_2(filename: Path):
    """Part two of day 18. (largest magnitude)"""
    with filename.open("r") as file:
        lines = list(map(eval, file.read().splitlines()))
    print(
        "The largest magnitude of any sum of two different snailfish numbers is:",
        max(magnitude(add(a, b)) for a, b in itertools.permutations(lines, 2)),
    )


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
