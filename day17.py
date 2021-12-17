"""Solution for Advent of Code day 17."""
from pathlib import Path
import re
import sys
import doctest
import click


def read_target_area(filename: Path) -> tuple[int, int, int, int]:
    """Read the target area of the probe

    Args:
        filename (Path): path to the input file.

    Returns:
        tuple[int]:  x_start, x_stop, y_start, y_stop

    Examples:
        >>> read_target_area(Path("test_data/day_17.data"))
        (20, 30, -10, -5)
    """
    find_target = re.compile(
        r"x=([0-9]*)\.\.([0-9]*), y=(-?(?:[0-9]*))\.\.(-?(?:[0-9]*))"
    )
    with filename.open("r") as file:
        target = find_target.search(file.read())
    return (
        int(target.group(1)),
        int(target.group(2)),
        int(target.group(3)),
        int(target.group(4)),
    )


def find_possible_velocities(
    target: tuple[int, int, int, int],
    search_space: int = 200,
    max_expected_y: int = 10000,
) -> tuple[int, int]:
    """Find initial velocities that would end up in the target area

    Args:
        target (tuple[int,int,int,int]): target area (x_start, x_stop, y_start, y_stop)
        search_space (int): max search space (limits the search range)
            (default = 500)
        max_expected_y (int): max y value we expect (limits the search range)
            (default = 10000)

    Returns:
        int: max reachable y
        int: number of possible shots that would end up in the target

    Examples:
        >>> find_possible_velocities((20, 30, -10, -5))
        (45, 112)
        >>> find_possible_velocities((20, 30, -10, -5), search_space = 500)
        (45, 112)
        >>> find_possible_velocities((135, 155, -102, -78))
        (5151, 968)
        >>> find_possible_velocities((135, 155, -102, -78), search_space = 100)
        (-25, 177)
    """
    max_y = -sys.maxsize - 1
    num_in_target = 0
    for x in range(0, search_space):
        for y in range(-search_space, search_space):
            cur_x = 0
            cur_y = 0
            velocity_x = x
            velocity_y = y
            current_max_y = -sys.maxsize - 1

            # Make sure to set the bounds to a reasonable number...
            while (
                -search_space <= cur_x <= search_space
                and -search_space <= cur_y <= max_expected_y
            ):
                cur_x += velocity_x
                cur_y += velocity_y
                current_max_y = max(current_max_y, cur_y)

                velocity_y -= 1
                if velocity_x > 0:
                    velocity_x -= 1
                elif velocity_x < 0:
                    velocity_x += 1

                if target[0] <= cur_x <= target[1] and target[2] <= cur_y <= target[3]:
                    max_y = max(max_y, current_max_y)
                    num_in_target += 1
                    break
    return max_y, num_in_target


@click.group()
def main():
    """CLI for the solution of day 17

    Advent of code 2021 (https://adventofcode.com/2021/day/17)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_17.data"),
)
def solve(filename: Path):
    """Part one and two of day 17."""
    max_y, num_in_target = find_possible_velocities(read_target_area(filename))
    print(f"A trick shot would result in a max height of : {max_y}")
    print(
        f"There are {num_in_target} initial velocities that would bring the "
        "probe into the target area"
    )


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
