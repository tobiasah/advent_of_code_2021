"""Solution for Advent of Code day 19."""
from collections import defaultdict
from pathlib import Path
from itertools import permutations
import doctest
import click

BeaconPosition = tuple[int]


def read_scanners(filename: Path) -> list[list]:
    """Read the raw scanner inputs.

    Args:
        filename (Path): filename

    Returns:
        list[list] scanned beacon positions for each scanner
    """
    result = []
    with filename.open("r") as file:
        for line in file:
            if "scanner" in line:
                result.append([])
            else:
                pos = list(
                    map(
                        int,
                        "".join(c if c in "1234567890-" else " " for c in line).split(),
                    )
                )
                if len(pos) == 3:
                    result[-1].append(tuple(pos))
    return result


def calculate_potential_beacon_positions(
    initial_beacon_positions: list[BeaconPosition],
):
    """Creates a list of all real possible beacone positions

    Scanners don`t know their rotation or facing direction. This function
    calculates for possible scenarios the beacon positions.

    Args:
        initial_beacon_positions (list[BeaconPosition]): provided initial postions

    Results:
        list[list[BeaconPosition]] : all possible permutations
    """
    res = []
    for permutation in permutations([0, 1, 2]):
        ii = [i for i in permutation if i != permutation[i]]
        ks = (
            [[], [0, 1], [0, 2], [1, 2]] if len(ii) != 2 else [[0], [1], [2], [0, 1, 2]]
        )
        for k in ks:
            l = []
            for pt in initial_beacon_positions:
                l.append(
                    tuple(pt[permutation[i]] * (-1 if i in k else 1) for i in range(3))
                )
            res.append(l)
    return res


def sub_vectors(a, b):
    """Subtracts two vectors.

    Args:
        pos1 (tuple[int]): first position
        pos1:(tuple[int]): second position

    Returns:
        tuple[int]: element wise subtraction

    Examples:
        >>> sub_vectors((1,4,6), (1,3,7))
        (0, 1, -1)
    """
    return tuple(a[i] - b[i] for i in range(3))


def add_vectors(pos1: tuple[int], pos2: tuple[int]) -> tuple[int]:
    """Adds two vectors.

    Args:
        pos1 (tuple[int]): first position
        pos1:(tuple[int]): second position

    Returns:
        tuple[int]: element wise sum

    Examples:
        >>> add_vectors((1,4,6), (1,3,7))
        (2, 7, 13)
    """
    return tuple(pos1[i] + pos2[i] for i in range(3))


def manhatten_distance(pos1: tuple[int], pos2: tuple[int]) -> int:
    """Calculate the manhattan distance for 2 points.

    Args:
        pos1 (tuple[int]): first position
        pos1:(tuple[int]): second position

    Returns:
        int: manhattan distance

    Examples:
        >>> manhatten_distance((1105,-1205,1229), (-92,-2380,-20))
        3621
    """
    return sum(abs(x) for x in sub_vectors(pos1, pos2))


def process_scanners(scanner_input: list[list]):
    """process the scanner inputs."""
    # [axis, scanner_pos, beacons]
    found = [(0, (0, 0, 0), scanner_input[0])]
    for _, _, scanned_beacon_positions in found:
        for axis, local_beacon_postions in enumerate(scanner_input):
            if axis not in [f[0] for f in found]:
                for (
                    potential_local_beacon_postions
                ) in calculate_potential_beacon_positions(local_beacon_postions):
                    diffs = defaultdict(list)
                    for i, pos_original in enumerate(scanned_beacon_positions):
                        for j, pos_found in enumerate(potential_local_beacon_postions):
                            diffs[sub_vectors(pos_original, pos_found)].append((i, j))
                    for potential_scanner_pos in diffs:
                        if len(diffs[potential_scanner_pos]) >= 12:
                            found.append(
                                (
                                    axis,
                                    potential_scanner_pos,
                                    [
                                        add_vectors(y, potential_scanner_pos)
                                        for y in potential_local_beacon_postions
                                    ],
                                )
                            )
                            break
                    else:
                        continue
                    break
    return found


@click.group()
def main():
    """CLI for the solution of day 19

    Advent of code 2021 (https://adventofcode.com/2021/day/19)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_19.data"),
)
def part_1(filename: Path):
    """Part one of day 19. (num of beacons)"""
    found = process_scanners(read_scanners(filename))
    found_beacons = set()
    for _, _, beacons in found:
        found_beacons = found_beacons.union(set(beacons))
    print(f"{len(found_beacons)} beacons found.")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_19.data"),
)
def part_2(filename: Path):
    """Part two of day 19. (max distance)"""
    found = process_scanners(read_scanners(filename))
    max_manhattan_dist = 0
    for _, scanner_pos, _ in found:
        for _, scanner_pos_2, _ in found:
            max_manhattan_dist = max(
                [max_manhattan_dist, manhatten_distance(scanner_pos, scanner_pos_2)]
            )
    print(f"The max manhattan distance between two scanners is {max_manhattan_dist}")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
