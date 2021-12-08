"""Solution for Advent of Code day 8."""
from pathlib import Path
from typing import Iterator
import doctest
import click

def read_as_block_output(filename: Path) -> Iterator[list[int]]:
    """Generator thats yield the encoded reference and output number for each line

    Args:
        filename (Path): path to the input file.

    Yields:
        (list, list): encoded reference, encoded output number

    Examples:
        >>> next(read_as_block_output(Path("test_data/day_8.data")))
        (['be', 'cfbegad', 'cbdgef', 'fgaecd', 'cgeb', 'fdcge', 'agebfd', 'fecdb', 'fabcd', 'edb'], ['fdgacbe', 'cefdb', 'cefbgd', 'gcbe'])
    """
    with filename.open("r") as file:
        for line in file:
            input_values = line.strip().split(" | ")
            output_values = input_values[1]
            input_values = input_values[0]
            yield input_values.split(" "), output_values.split(" ")


def find_mapping(reference: list[str]) -> map:
    """creates segment mapping for encoded digits.

    The reference must contain for each number between 0 and 9 the encoded segments.
    The algorithm creates a mapping that tells for each encoded segment the decoded one.

    Args:
        reference (list[str]): encoded references (encoded values 0-9)

    Returns:
        (map) map that encodes each segment.

    Examples:
        >>> find_mapping(["be", "cfbegad", "cbdgef", "fgaecd", "cgeb", "fdcge", "agebfd", "fecdb", "fabcd", "edb"])
        {'e': 'f', 'b': 'c', 'd': 'a', 'g': 'b', 'c': 'd', 'f': 'g', 'a': 'e'}
        >>> find_mapping(["edbfga", "begcd", "cbg", "gc", "gcadebf", "fbgde", "acbgfd", "abcde", "gfcbed", "gfec"])
        {'g': 'f', 'c': 'c', 'b': 'a', 'f': 'b', 'e': 'd', 'd': 'g', 'a': 'e'}
    """

    result = {}

    # search for one
    for digit in reference:
        if len(digit) == 2:
            c_f_option = digit
    assert len(c_f_option) == 2, c_f_option

    # search for six
    for digit in reference:
        if len(digit) == 6 and (c_f_option[0] in digit) != (c_f_option[1] in digit):
            if c_f_option[0] in digit:
                result[c_f_option[0]] = "f"
                result[c_f_option[1]] = "c"
            else:
                result[c_f_option[1]] = "f"
                result[c_f_option[0]] = "c"
    assert len(result) == 2, f"result={result} c_f_option={c_f_option} {reference}"

    # search for seven
    for digit in reference:
        if len(digit) == 3:
            for segment in digit:
                if segment not in c_f_option:
                    result[segment] = "a"
    assert len(result) == 3, f"result={result}"

    # search for four
    for digit in reference:
        if len(digit) == 4:
            b_d_option = ""
            for segment in digit:
                if segment not in c_f_option:
                    b_d_option += segment
    assert len(b_d_option) == 2, b_d_option

    # search for zero
    # 0 has 6 segments and is missing either b or d. (=> if b is present d is missing)
    for digit in reference:
        if len(digit) == 6 and (b_d_option[0] in digit) != (b_d_option[1] in digit):
            if b_d_option[0] in digit:
                result[b_d_option[0]] = "b"
                result[b_d_option[1]] = "d"
            else:
                result[b_d_option[1]] = "b"
                result[b_d_option[0]] = "d"
    assert len(result) == 5, f"result={result}"

    # search for nine
    # 9 has 6 segments and is missing either e or g. (=> if e is present g is missing)
    e_g_option = ""
    for segment in ["a", "b", "c", "d", "e", "f", "g"]:
        if segment not in result:
            e_g_option += segment
    assert len(e_g_option) == 2, e_g_option

    for digit in reference:
        if len(digit) == 6 and (e_g_option[0] in digit) != (e_g_option[1] in digit):
            if e_g_option[0] in digit:
                result[e_g_option[0]] = "g"
                result[e_g_option[1]] = "e"
            else:
                result[e_g_option[1]] = "g"
                result[e_g_option[0]] = "e"
    assert len(result) == 7, f"result={result}"
    return result


def decode(encoded_digits: list[str], mapping: dict) -> int:
    """decode a number.

    Use the mapping to decode the encoded digits and combine them to a number.

    Args:
        encoded_digits (list[str]): encoded digits
        mapping (dict): mapping that decodes each segment

    Returns:
        (int) decoded number

    Examples:
        >>> decode(["cf", "fc", "acf"], {"a":"a", "c":"c", "f":"f"})
        117
        >>> decode(["cb", "bc", "acb"], {"a":"a", "c":"c", "b":"f"})
        117
        >>> decode(["fcdb", "bc", "acb"], {"a":"a", "b":"f", "c":"c", "d":"d", "f":"b"})
        417
    """
    digits = {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9",
    }
    result = ""
    for digit in encoded_digits:
        decoded_segments = ""
        for segment in digit:
            decoded_segments += mapping[segment]
        decoded_segments = "".join(sorted(decoded_segments))
        result += digits[decoded_segments]
    return int(result)


@click.group()
def main():
    """CLI for the solution of day 8

    Advent of code 2021 (https://adventofcode.com/2021/day/8)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_8.data"),
)
def part_1(filename: Path):
    """Part one of day day. (count easy digits)"""
    counter = 0
    for _, output_values in read_as_block_output(filename):
        for digit in output_values:
            if len(digit) in [2, 3, 4, 7]:
                counter += 1
    print(f"There are {counter} easy to detect digits in the data.")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_8.data"),
)
def part_2(filename: Path):
    """Part two of day three. (life support rating)"""
    summe = 0
    for input_values, output_values in read_as_block_output(filename):
        summe += decode(output_values, find_mapping(input_values))

    print(f"The sum of the decoded outputs is: {summe}.")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
