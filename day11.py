"""Solution for Advent of Code day 11."""
from pathlib import Path
import doctest
import click


def read_energy_grid(filename: Path) -> list[list[int]]:
    """Read energy grid from file

    Args:
        filename (Path): path to the input file.

    Returns:
    list[list[int]] Energy field

    Examples:
        >>> x = [print(line) for line in read_energy_grid(Path("test_data/day_11.data"))]
        [5, 4, 8, 3, 1, 4, 3, 2, 2, 3]
        [2, 7, 4, 5, 8, 5, 4, 7, 1, 1]
        [5, 2, 6, 4, 5, 5, 6, 1, 7, 3]
        [6, 1, 4, 1, 3, 3, 6, 1, 4, 6]
        [6, 3, 5, 7, 3, 8, 5, 4, 7, 8]
        [4, 1, 6, 7, 5, 2, 4, 6, 4, 5]
        [2, 1, 7, 6, 8, 4, 1, 7, 2, 1]
        [6, 8, 8, 2, 8, 8, 1, 1, 3, 4]
        [4, 8, 4, 6, 8, 4, 8, 5, 5, 4]
        [5, 2, 8, 3, 7, 5, 1, 5, 2, 6]
    """
    grid = []
    with filename.open("r") as file:
        for line in file:
            grid.append([int(x) for x in line.strip()])
    return grid


def flash_octopus(
    row: int, col: int, grid: list[list[int]]
) -> tuple[list[list[int]], int]:
    """Flashes single occtopus. (recursively)

    If the flash of an occtopus causes another occtopus to flash the function
    is called recursivly.
    The energy level of the flashed occtopus is reset to -1 to prevent multiple
    flashing.

    Args:
        row (int): row of flashing occtopus
        col (int): column of flashing occtopus
        grid (list[list[int]]): energy grid

    Returns:
        list[list[int]]: updated energy grid
        int:    number of flashes

    Examples:
        >>> flash_octopus(1,1,[[1,1,1],[1,10,1],[1,1,1]])
        ([[2, 2, 2], [2, -1, 2], [2, 2, 2]], 1)
        >>> flash_octopus(1,1,[[9,1,9],[6,10,8],[8,9,7]])
        ([[-1, 6, -1], [-1, -1, -1], [-1, -1, -1]], 8)
    """
    num_row = len(grid)
    num_col = len(grid[0])
    flashes = 1
    grid[row][col] = -1
    for delta_row in [-1, 0, 1]:
        for delta_col in [-1, 0, 1]:
            row_adjacent = row + delta_row
            col_adjacent = col + delta_col
            if (
                0 <= row_adjacent < num_row
                and 0 <= col_adjacent < num_col
                and grid[row_adjacent][col_adjacent] != -1
            ):
                grid[row_adjacent][col_adjacent] += 1
                if grid[row_adjacent][col_adjacent] >= 10:
                    grid, flashes_child = flash_octopus(
                        row_adjacent, col_adjacent, grid
                    )
                    flashes += flashes_child
    return grid, flashes


def simulate_round(grid: list[list[int]]) -> tuple[list[list[int]], int, bool]:
    """Simulate a single round.

    * First, the energy level of each octopus increases by 1.
    * Then, any octopus with an energy level greater than 9 flashes. This
      increases the energy level of all adjacent octopuses by 1, including
      octopuses that are diagonally adjacent. If this causes an octopus to
      have an energy level greater than 9, it also flashes. This process
      continues as long as new octopuses keep having their energy level
      increased beyond 9. (An octopus can only flash at most once per step.)
    * Finally, any octopus that flashed during this step has its energy level
      set to 0, as it used all of its energy to flash.

    Args:
        grid (list[list[int]]): energy grid

    Returns:
        list[list[int]]: updated energy grid.
        int:             number of flashes.

    Examples:
        >>> simulate_round([[0,0,0],[0,9,0],[0,0,0]])
        ([[2, 2, 2], [2, 0, 2], [2, 2, 2]], 1)
        >>> simulate_round([[8,0,8],[5,9,7],[7,8,6]])
        ([[0, 6, 0], [0, 0, 0], [0, 0, 0]], 8)
        >>> simulate_round([[8,9,8],[8,9,7],[9,8,8]])
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 9)
    """
    sum_flashes = 0
    num_row = len(grid)
    num_col = len(grid[0])
    for row in range(num_row):
        for col in range(num_col):
            grid[row][col] += 1
    for row in range(num_row):
        for col in range(num_col):
            if grid[row][col] >= 10:
                grid, flashes = flash_octopus(row, col, grid)
                sum_flashes += flashes
    for row in range(num_row):
        for col in range(num_row):
            if grid[row][col] == -1:
                grid[row][col] = 0
    return grid, sum_flashes


@click.group()
def main():
    """CLI for the solution of day 11

    Advent of code 2021 (https://adventofcode.com/2021/day/11)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_11.data"),
)
def part_1(filename: Path):
    """Part one of day 11. (sum flashes)"""
    grid = read_energy_grid(filename)
    sum_flashes = 0
    for _ in range(100):
        grid, flashes = simulate_round(grid)
        sum_flashes += flashes

    print(f"After 100 rounds there has been {sum_flashes} flashes.")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_11.data"),
)
def part_2(filename: Path):
    """Part two of day ten. (numer of round before sync)"""

    grid = read_energy_grid(filename)
    octopuses = len(grid) * len(grid[0])
    num_rounds = 0
    while True:
        num_rounds += 1
        grid, flashes = simulate_round(grid)
        if flashes == octopuses:
            break
    print(f"Octopuses synced after {num_rounds} rounds.")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
