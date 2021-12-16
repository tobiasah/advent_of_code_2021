"""Solution for Advent of Code day 16."""
import doctest
from pathlib import Path
import click


def read_message(filename: Path) -> tuple[dict, str]:
    """Read polymer structure information from a file

    The polymer is represented by a dict of rules and a polymer structer.

    Args:
        filename (Path): path to the input file.

    Returns:
        dict:   rules
        str:    initial polymer structure

    Examples:
        >>> read_message(Path("test/day_16.data"))[0:15]
        '000000100000110'
    """
    with filename.open("r") as file:
        hex_data = file.read().strip()
    binary_data = bin(int(hex_data, 16))[2:]
    while len(binary_data) < 4 * len(hex_data):
        binary_data = "0" + binary_data
    return binary_data


sum_versions = 0


def parse_bits_transmission(
    bits: list[str], pos: int = 0, indent: int = 0
) -> tuple[int, int]:
    """Parse a message accoring to the Buoyancy Interchange Transmission System (BITS)

    Args:
        bits (list[str]): message in binary representation
        pos (int): current position in the bit stream
        indent (int): curent indentation

    Returns:
        int: current value of the packet
        int: position of next message

    Examples:
        >>> parse_bits_transmission("110100101111111000101000")
        (2021, 21)
        >>> parse_bits_transmission("110100101111101000101000")
        (1957, 21)
        >>> parse_bits_transmission("110100101100111000101000")
        (110, 16)
    """
    global sum_versions
    version = int(bits[pos + 0 : pos + 3], 2)
    sum_versions += version
    packet_type = int(bits[pos + 3 : pos + 6], 2)
    if packet_type == 4:  # literal value
        pos += 6
        value = 0
        while True:
            value = value * 16 + int(bits[pos + 1 : pos + 5], 2)
            pos += 5
            if bits[pos - 5] == "0":
                return value, pos
    else:  # operator
        values = []
        if int(bits[pos + 6], 2) == 0:
            # the next 15 bits are a number that represents the total length in
            # bits of the sub-packets contained by this packet.
            len_bits = int(bits[pos + 7 : pos + 7 + 15], 2)
            start_i = pos + 7 + 15
            pos = start_i
            while True:
                value, next_i = parse_bits_transmission(bits, pos, indent + 1)
                values.append(value)
                pos = next_i
                if pos - start_i == len_bits:
                    break
        else:
            # the next 11 bits are a number that represents the number of
            # sub-packets immediately contained by this packet.
            num_sub_packets = int(bits[pos + 7 : pos + 7 + 11], 2)
            pos += 7 + 11
            for _ in range(num_sub_packets):
                sub_version, next_i = parse_bits_transmission(bits, pos, indent + 1)
                values.append(sub_version)
                pos = next_i
        # Apply operator
        if packet_type == 0:
            return sum(values), pos
        elif packet_type == 1:
            ans = 1
            for value in values:
                ans *= value
            return ans, pos
        elif packet_type == 2:
            return min(values), pos
        elif packet_type == 3:
            return max(values), pos
        elif packet_type == 5:
            return (1 if values[0] > values[1] else 0), pos
        elif packet_type == 6:
            return (1 if values[0] < values[1] else 0), pos
        elif packet_type == 7:
            return (1 if values[0] == values[1] else 0), pos
        else:
            assert False, packet_type


@click.group()
def main():
    """CLI for the solution of day 16

    Advent of code 2021 (https://adventofcode.com/2021/day/16)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test/day_16.data"),
)
def part_1(filename: Path):
    """Part one of day 16. (sum_versions)"""
    global sum_versions
    _, _ = parse_bits_transmission(read_message(filename), 0, 0)
    print(f"The sum of all versions is: {sum_versions}")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test/day_16.data"),
)
def part_2(filename: Path):
    """Part two of day 16. (evaluate the BITS transmission)"""
    value, _ = parse_bits_transmission(read_message(filename), 0, 0)
    print(f"The value of the BITS transmission is {value}")


@main.command()
def test():
    """run doctest."""
    print(doctest.testmod())


if __name__ == "__main__":
    main()
