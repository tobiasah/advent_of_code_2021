"""Solution for Advent of Code day 6."""
from pathlib import Path
import doctest
import click


def read_distribution(filename: Path) -> list[int]:
    """Read file as interger list and convert it into a distribution

    Warning: No sanity check for the input is done.

    The distribution accepts values from zero to 8.

    Args:
        filename (Path): path to the input file.

    Returns:
        list[int] distribution between 0 and 9

    Examples:
        >>> read_distribution(Path("test_data/day_6.data"))
        [0, 1, 1, 2, 1, 0, 0, 0, 0]
    """
    initial_values = []
    initial_dist = [0] * 9
    with filename.open("r") as file:
        initial_values = file.read().split(",")
    for value in initial_values:
        initial_dist[int(value)] += 1
    return initial_dist


def progress_population(
    days: int, distribution: list[int], respawn_offset: int = 6
) -> list[int]:
    """Progress a population by a defines number of days.

    The function has the following assumtions:
        * no object dies or is removed
        * the distribution defines how many days are left until the object respawns
        * every time an object respawns it creates a new object a the end of the
          distribution

    Args:
        days (int): Number of days the population should be progressed
        distribution (list[int]): Distribution of the population that indicates.
            the remaining days until an object respawns.
        respawn_offset (int): Offset an object will respawn to.

    Returns:
        (list[int]): Progressed distribution.

    Examples:
        >>> progress_population(1, [0,1])
        [1, 0, 0, 0, 0, 0, 0, 0]
        >>> progress_population(1, [0,1], respawn_offset = 1)
        [1, 0, 0]
        >>> progress_population(2, [0,1])
        [0, 0, 0, 0, 0, 0, 1, 1]
        >>> progress_population(2, [0,1], respawn_offset = 1)
        [0, 1, 1]
        >>> progress_population(3, [0,1,0,0,0,0,0,0])
        [0, 0, 0, 0, 0, 1, 1, 0]
        >>> sum(progress_population(256, [0,1,1,2,1,0,0,0,0]))
        26984457539
    """
    offset = 0
    new_fish = 0
    max_spawn = len(distribution)
    if max_spawn <= respawn_offset + 1:
        distribution += [0] * (respawn_offset - max_spawn + 2)
        max_spawn = respawn_offset + 2

    for i in range(days):
        # resetted fish
        reset_offset = (offset + respawn_offset + 1) % max_spawn
        distribution[reset_offset] += distribution[offset]
        distribution[offset] = 0
        # new fish
        distribution[offset] += new_fish
        # progress
        offset = (offset + 1) % max_spawn
        new_fish = distribution[offset]

    new_dist = [0] * max_spawn
    for i in range(max_spawn):
        new_dist[i] = distribution[(offset + i) % max_spawn]
    return new_dist


@click.group()
def main():
    """CLI for the solution of day 6

    Advent of code 2021 (https://adventofcode.com/2021/day/6)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_6.data"),
)
@click.argument(
    "days",
    required=False,
    type=int,
    default=80,
)
def solution(filename: Path, days: int):
    """Soulution for day 6.
    Part 1 -> days = 80, Part 2 -> days = 256.
    """
    counter_list = progress_population(days, read_distribution(filename))
    print(f"Population after {days} days = {sum(counter_list)}")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
