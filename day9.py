"""Solution for Advent of Code day 9."""
from pathlib import Path
from collections import deque
import doctest
import click


def read_height_map(filename: Path) -> list[list[int]]:
    """read height map from file

    Args:
        filename (Path): path to the input file.

    Returns:
        list[list[int]] heightmap

    Examples:
        >>> read_height_map(Path("test_data/day_9.data"))[0]
        [2, 1, 9, 9, 9, 4, 3, 2, 1, 0]
    """
    height_map = []
    with filename.open("r") as file:
        for line in file:
            height_map.append([int(x) for x in list(line.strip())])
    return height_map


def find_risk_levels(height_map: list[list[int]]) -> list[int]:
    """Find the risk levels of the low poin in a hightmap

    Args:
        height_map (list[list[int]): heighmap

    Returns:
        list[int] riks levels or all local minima

    Examples:
        >>> find_risk_levels([[1,1,1],[1,0,1],[1,1,1]])
        [1]
        >>> find_risk_levels([[0,5,7,1],[1,0,8,1],[7,8,9,1],[1,6,1,1]])
        [1, 1, 2]
    """
    num_rows = len(height_map)
    num_cols = len(height_map[0])
    delta_row = [-1, 0, 1, 0]
    delta_col = [0, 1, 0, -1]

    risk_levels = []
    for row in range(num_rows):
        assert len(height_map[row]) == num_cols
        for column in range(num_cols):
            is_local_min = True
            for d in range(4):
                neighbour_row = row + delta_row[d]
                neighbour_col = column + delta_col[d]
                if (
                    0 <= neighbour_row < num_rows
                    and 0 <= neighbour_col < num_cols
                    and height_map[neighbour_row][neighbour_col]
                    <= height_map[row][column]
                ):
                    is_local_min = False
            if is_local_min:
                risk_levels.append(height_map[row][column] + 1)
    return risk_levels

def find_size_basins(height_map: list[list[int]]):
    """Find the sizes of all basins in a hightmap

    Args:
        height_map (list[list[int]): heighmap

    Returns:
        list[int] size or all local maxima

    Examples:
        >>> find_size_basins([[1,1,1],[1,0,1],[1,1,1]])
        [9]
        >>> find_size_basins([[0,5,7,1],[1,0,8,1],[7,8,9,1],[1,6,1,1]])
        [15]
    """
    num_rows = len(height_map)
    num_cols = len(height_map[0])
    delta_row = [-1, 0, 1, 0]
    delta_col = [0, 1, 0, -1]
    basins_sizes = []
    seen_fields = set()
    for row in range(num_rows):
        for column in range(num_cols):
            if (row,column) not in seen_fields and height_map[row][column]!=9:
                size = 0
                queue = deque()
                queue.append((row,column))
                while queue:
                    (row,column) = queue.popleft()
                    if (row,column) in seen_fields:
                        continue
                    seen_fields.add((row,column))
                    size += 1
                    for d in range(4):
                        neighbour_row = row+delta_row[d]
                        neighbour_col = column+delta_col[d]
                        if 0<=neighbour_row<num_rows and 0<=neighbour_col<num_cols and height_map[neighbour_row][neighbour_col]!=9:
                            queue.append((neighbour_row,neighbour_col))
                basins_sizes.append(size)
    basins_sizes.sort()
    return basins_sizes


@click.group()
def main():
    """CLI for the solution of day 9

    Advent of code 2021 (https://adventofcode.com/2021/day/9)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_9.data"),
)
def part_1(filename: Path):
    """Part one of day nine. (sum risk level)"""
    sum_risk_level = find_risk_levels(read_height_map(filename))
    print(f"The sum of teh risk level of all local minima is {sum(sum_risk_level)}")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_9.data"),
)
def part_2(filename: Path):
    """Part two of day nine. (sum basin size)"""
    basins = find_size_basins(read_height_map(filename))

    print(f"The sum of the 3 largest basins is: {basins[-1]*basins[-2]*basins[-3]}.")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
