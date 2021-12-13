"""Solution for Advent of Code day 12."""
from pathlib import Path
from collections import defaultdict, deque
import doctest
import click


def read_adjacency_list(filename: Path) -> dict[list[str]]:
    """create a dict with all adjacents for each cave.
    Args:
        filename (Path): path to the input file.

    Returns:
    dict[list[str]] adjacency list for all caves

    Examples:
        >>> x = [print(f"{k},{v}") for k,v in read_adjacency_list(Path("test_data/day_12.data")).items()]
        dc,['end', 'start', 'HN', 'LN', 'kj']
        end,['dc', 'HN']
        HN,['start', 'dc', 'end', 'kj']
        start,['HN', 'kj', 'dc']
        kj,['start', 'sa', 'HN', 'dc']
        LN,['dc']
        sa,['kj']
    """
    adjacencies = defaultdict(list)
    with filename.open("r") as file:
        for line in file:
            a, b = line.strip().split("-")
            adjacencies[a].append(b)
            adjacencies[b].append(a)
    return adjacencies


def find_paths(adjacency_list: dict[list[str]], small_only_once: bool = True) -> int:
    """Find all paths through the caves.

    Args:
        adjacency_list (dict[list[str]]): adjacency list for all caves
        small_only_once (bool): Flag if small caves should only be visited once

    Returns:
        int: number of paths through the caves

    Examples:
        >>> find_paths({"start":["end"],"end":["start"]})
        1
        >>> find_paths({"start":["A"], "A":["start","end"], "b":["A"], "end":["A"]})
        1
    """
    path_queue = deque([("start", set(["start"]), None)])
    num_paths = 0
    while path_queue:
        position, small, twice = path_queue.popleft()
        if position == "end":
            num_paths += 1
            continue
        for adjacent in adjacency_list[position]:
            if adjacent not in small:
                new_small = set(small)
                if adjacent.lower() == adjacent:
                    new_small.add(adjacent)
                path_queue.append((adjacent, new_small, twice))
            elif (
                adjacent in small
                and twice is None
                and adjacent not in ["start", "end"]
                and not small_only_once
            ):
                path_queue.append((adjacent, small, adjacent))
    return num_paths


@click.group()
def main():
    """CLI for the solution of day 12

    Advent of code 2021 (https://adventofcode.com/2021/day/12)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_12.data"),
)
def part_1(filename: Path):
    """Part one of day 12. (small caves once)"""
    num_paths = find_paths(read_adjacency_list(filename))

    print(f"If one only visits small caves once there are {num_paths} paths.")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_12.data"),
)
def part_2(filename: Path):
    """Part two of day 12. (all paths)"""
    num_paths = find_paths(read_adjacency_list(filename), False)

    print(f"There are {num_paths} paths through the caves.")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
