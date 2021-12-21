"""Solution for Advent of Code day 20."""
from pathlib import Path
import doctest
import click


def read_input(filename: Path) -> tuple[str, set[int, int]]:
    """read the input from the scanners.

    Args:
        filename (Path): filename

    Returns:
        str : rules
        set[int,int]: input image
    """
    with filename.open("r") as file:
        data = file.read().strip()

    rule, start = data.split("\n\n")
    rule = rule.strip()

    input_image = set()
    for row, line in enumerate(start.strip().split("\n")):
        for col, x in enumerate(line.strip()):
            if x == "#":
                input_image.add((row, col))
    return rule, input_image


def apply_image_enhancement(image: set[int, int], on: bool, rule: str) -> set[int, int]:
    """Applies the image enhancement to the image.

    Args:
        image (set[int,int]): input image
        on (bool): Flag that indicates if the pixel in image indecates on or off
        rule(str): image engancement rules

    Returns:
        set[int,int] processed image
    """
    result = set()
    row_low = min([row for row, _ in image])
    row_high = max([row for row, _ in image])
    col_low = min([col for _, col in image])
    col_high = max([col for _, col in image])
    for row in range(row_low - 5, row_high + 10):
        for col in range(col_low - 5, col_high + 10):
            row_col_str = 0
            bit = 8
            for delta_row in [-1, 0, 1]:
                for delta_col in [-1, 0, 1]:
                    if ((row + delta_row, col + delta_col) in image) == on:
                        row_col_str += 2 ** bit
                    bit -= 1
            assert 0 <= row_col_str < 512
            if (rule[row_col_str] == "#") != on:
                result.add((row, col))
    return result


@click.group()
def main():
    """CLI for the solution of day 20

    Advent of code 2021 (https://adventofcode.com/2021/day/20)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_20.data"),
)
def part_1(filename: Path):
    """Part one of day 20. (2 runs)"""
    rule, image = read_input(filename)

    for i in range(2):
        image = apply_image_enhancement(image, i % 2 == 0, rule)
    print(f"{len(image)} pixels are lit after 2 rounds")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_20.data"),
)
def part_2(filename: Path):
    """Part two of day 20. (50 runs)"""
    rule, image = read_input(filename)

    for i in range(50):
        image = apply_image_enhancement(image, i % 2 == 0, rule)
    print(f"{len(image)} pixels are lit after 50 rounds")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
