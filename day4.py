"""Solution for Advent of Code day 4."""
from pathlib import Path
from typing import Iterable, Iterator
import doctest
import numpy as np
import click


class BingoBoard:
    """Bingo Board.

    Keeps track of the current status (hits) and can be used to check if a
    board is finished.

    Args:
        board (np.array) board.
    """

    def __init__(self, board: np.array):
        self._board = board
        self._row = [0] * 5
        self._col = [0] * 5
        self._hits = np.zeros(shape=(5, 5))

    def play_round(self, number: int) -> None:
        """Plays a round.

        Args:
            number (int): drawn number.

        Examples:
        >>> test_board.hits
        array([[1., 0., 0., 0., 0.],
               [1., 0., 0., 0., 0.],
               [1., 0., 0., 0., 0.],
               [1., 0., 0., 0., 0.],
               [1., 0., 0., 0., 0.]])
        >>> test_board.play_round(0)
        >>> test_board.hits
        array([[1., 0., 0., 0., 1.],
               [1., 0., 0., 0., 0.],
               [1., 0., 0., 0., 0.],
               [1., 0., 0., 0., 0.],
               [1., 0., 0., 0., 0.]])
        """
        index_row, index_col = np.where(self._board == number)
        if len(index_row) > 1 or len(index_col) > 1:
            raise Exception
        if len(index_row) != 0 and len(index_col) != 0:
            index_row, index_col = index_row[0], index_col[0]
            self._row[index_row] += 1
            self._col[index_col] += 1
            self._hits[index_row][index_col] = 1

    def is_finished(self) -> bool:
        """Check if a board is finished.

        Returns:
            (bool) finished?
        Examples:
            >>> test_board.is_finished()
            False
            >>> test_board.play_round(22)
            >>> test_board.play_round(8)
            >>> test_board.play_round(21)
            >>> test_board.play_round(6)
            >>> test_board.play_round(1)
            >>> test_board.is_finished()
            True

        """
        return 5 in self._row or 5 in self._col

    @property
    def board(self) -> np.array:
        """Board."""
        return self._board

    @property
    def hits(self) -> np.array:
        """matrix with hits. (1 = hit 0 = no hit)."""
        return self._hits


def read_boards(file_content: Iterable) -> Iterator[BingoBoard]:
    """read lines from file and convert them to bingo boards.

    Empty lines are considered as board seperators.
    WARNING: There is no sanity check if the raw input boards is a square.
             Missing lines will be filled with zeros.

    Args:
        file_content (Iterable): iterator for the lines to parse.

    Yields:
        BingoBoard: single board for bingo.

    Examples:
        >>> next(read_boards(["22 13 17 11  0"," 8  2 23  4 24"])).board
        array([[22., 13., 17., 11.,  0.],
               [ 8.,  2., 23.,  4., 24.],
               [ 0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.]])
    """
    field = np.zeros(shape=(5, 5))
    colum_counter = 0
    for line in file_content:
        line = line.strip()
        if not line:
            if colum_counter:
                yield BingoBoard(field)
            field = np.zeros(shape=(5, 5))
            colum_counter = 0
            continue
        line = [int(character) for character in line.split(" ") if character]
        field[colum_counter] = line
        colum_counter += 1
    yield BingoBoard(field)


def read_bingo_game(filename: Path) -> tuple[list[int], list[BingoBoard]]:
    """Read a bingo game from a file.

    Args:
        filename (Path): path to the input file.

    Returns:
        (list[int], list[BingoBoard]) drawn numbers, bingo boards
    """
    with filename.open("r") as file:
        numbers = next(file)
        numbers = numbers.strip().split(",")
        numbers = [int(character) for character in numbers]
        boards = list(read_boards(file))
        return numbers, boards


def calc_score(board: BingoBoard, number: int) -> int:
    """Calculate the current score of a Bingo Board.

    Args:
        board (BingoBoard): Bingo board
        number (int): number that was drawn.

    Returns:
        (int) Score of that board
    """
    summe = 0
    for index_row, row in enumerate(board.hits):
        for index_col, hit in enumerate(row):
            if not hit:
                summe += board.board[index_row][index_col]
    return number * summe


@click.group()
def main():
    """CLI for the solution of day 4

    Advent of code 2021 (https://adventofcode.com/2021/day/4)
    """


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_4.data"),
)
def part_1(filename: Path):
    """Part one of day four. (find winning board)"""
    numbers, boards = read_bingo_game(filename)

    for number_counter, number in enumerate(numbers):
        for board_counter, board in enumerate(boards):
            board.play_round(number)
            if board.is_finished():
                score = calc_score(board, number)
                print(
                    f"board {board_counter} wins after {number_counter} "
                    f"numbers ({number}) with score: {int(score)}"
                )
                return
    print("No winner after the given drawed numbers.")


@main.command()
@click.argument(
    "filename",
    required=False,
    type=Path,
    default=Path("test_data/day_4.data"),
)
def part_2(filename: Path):
    """Part two of day four. (find loosing board)"""
    numbers, boards = read_bingo_game(filename)

    winner = [0] * len(boards)
    for number_counter, number in enumerate(numbers):
        board_counter = 0
        for board_counter, board in enumerate(boards):
            if winner[board_counter] == 0:
                board.play_round(number)
                if board.is_finished():
                    winner[board_counter] = 1
                    if sum(winner) == len(boards):
                        score = calc_score(board, number)
                        print(
                            f"board {board_counter} finishes last after "
                            f"{number_counter} numbers ({number}) with score: "
                            f"{int(score)}"
                        )
                        return

    unfinished_boards = [i for i, boards in enumerate(winner) if boards == 0]
    print(f"There are multiple boards that are not finished {unfinished_boards}")


@main.command()
def test():
    """run doctest."""
    print(
        doctest.testmod(
            extraglobs={
                "test_board": BingoBoard(
                    np.array(
                        [
                            [22.0, 13.0, 17.0, 11.0, 0.0],
                            [8.0, 2.0, 23.0, 4.0, 24.0],
                            [21.0, 9.0, 14.0, 16.0, 7.0],
                            [6.0, 10.0, 3.0, 18.0, 5.0],
                            [1.0, 12.0, 20.0, 15.0, 19.0],
                        ]
                    )
                )
            }
        )
    )


if __name__ == "__main__":
    main()
