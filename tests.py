import time

import board
import puzzle
from solver import make_window, solve

win = make_window()


def random_puzzle_test():
    for test in puzzle.read_random_puzzles("not_super_easy.csv", 10):
        test.win = win
        test.draw()
        start = time.perf_counter()
        if solve(test, win):
            win.getMouse()
        print(time.perf_counter() - start)
        print("New")
        test.undraw()


def test_hidden_pairs():
    test = puzzle.Board(puzzle=[0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 4, 2, 7, 3, 0,
                                0, 0, 6, 7, 3, 0, 0, 4, 0,
                                0, 9, 4, 0, 0, 0, 0, 6, 8,
                                0, 0, 0, 0, 9, 6, 0, 0, 0,
                                0, 0, 7, 0, 0, 0, 0, 2, 3,
                                1, 0, 0, 0, 0, 0, 0, 8, 5,
                                0, 6, 0, 0, 8, 0, 2, 7, 1,
                                0, 0, 5, 0, 1, 0, 0, 9, 4], win=win)
    test.draw()
    solve(test, win)


def test_double_pairs():
    test = puzzle.Board(puzzle=[9, 3, 4, 0, 6, 0, 0, 5, 0,
                                0, 0, 6, 0, 0, 4, 9, 2, 3,
                                0, 0, 8, 9, 0, 0, 0, 4, 6,
                                8, 0, 0, 5, 4, 6, 0, 0, 7,
                                6, 0, 0, 0, 1, 0, 0, 0, 5,
                                5, 0, 0, 3, 9, 0, 0, 6, 2,
                                3, 6, 0, 4, 0, 1, 2, 7, 0,
                                4, 7, 0, 6, 0, 0, 5, 0, 0,
                                0, 8, 0, 0, 0, 0, 6, 3, 4], win=win)
    test.draw()
    solve(test, win=win, techniques=["Singles", "Double pairs"])


def test_iter_column():
    test = puzzle.Board(puzzle=[0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 4, 2, 7, 3, 0,
                                0, 0, 6, 7, 3, 0, 0, 4, 0,
                                0, 9, 4, 0, 0, 0, 0, 6, 8,
                                0, 0, 0, 0, 9, 6, 0, 0, 0,
                                0, 0, 7, 0, 0, 0, 0, 2, 3,
                                1, 0, 0, 0, 0, 0, 0, 8, 5,
                                0, 6, 0, 0, 8, 0, 2, 7, 1,
                                0, 0, 5, 0, 1, 0, 0, 9, 4], win=win)
    test.draw()
    for cell in test.get_board_per_column():
        print(cell.column)


def next_square_test():
    test = puzzle.read_random_puzzles("not_super_easy.csv", 10)[0]
    print(test.get_square('A'))
    for x in test.get_next_square('I'):
        print(x.square)


def square_offset_test():
    test = puzzle.read_random_puzzles("not_super_easy.csv", 10)[0]
    print(test.get_square('A'))
    for x in test.get_square_offset('A', down=1, right=1, up=1, left=99):
        print(x.square)


test_double_pairs()
# random_puzzle_test()
# test_iter_column()
