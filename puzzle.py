import random
from board import *

removed = 0
solutions = 1


def empty_spot(board):
    for cell in board:
        if cell.number == 0:
            return cell
    return None


def randomized(seq):
    shuffled = list(seq)
    random.shuffle(shuffled)
    return shuffled


def random_cell(board):
    for cell in randomized(board):
        if cell.number != 0:
            return cell
    return None


def random_numbers(board):
    numbers = board.possible_numbers.copy()
    random.shuffle(numbers)
    return numbers


def fill_board(board):
    cell = empty_spot(board)
    if cell is None:
        return True

    for number in random_numbers(board):
        if board.possible(cell, number):
            board.fill_in(cell, number)
            if fill_board(board):
                return True
            board.clear_cell(cell)
    return False


def solve_board(board):
    global solutions
    cell = empty_spot(board)

    for number in random_numbers(board):
        if board.possible(cell, number):
            board.fill_in(cell, number)
            if board.board_filled():
                solutions += 1
            elif solve_board(board):
                return True
            board.clear_cell(cell)


def remove_single(board):
    cell = random_cell(board)
    backup = cell.number
    board.clear_cell(cell)
    return cell, backup


def get_symmetric_cells(board):
    while True:
        cell = random_cell(board)
        row, col = cell.row - 1, cell.column - 1
        cell2 = board.cells[abs(row - 8)][abs(col - 8)]
        if cell2 != 0:
            return cell, cell2


def make_puzzle_symmetric(attempts):
    global solutions, removed
    removed = 0
    board = Board()
    fill_board(board)
    while attempts > 0:
        cell1, cell2 = get_symmetric_cells(board)
        backup = [cell1.number, cell2.number]
        board.clear_cell(cell1)
        board.clear_cell(cell2)
        removed += 2
        copy_board = Board(copy=board)
        solutions = 0
        solve_board(copy_board)
        if solutions != 1:
            board.fill_in(cell1, backup[0])
            board.fill_in(cell2, backup[1])
            removed -= 2
            attempts -= 1
    print(board)
    make_puzzle(15, board)
    print(board)
    return board


def make_puzzle(attempts, board=Board()):
    global solutions, removed
    fill_board(board)
    while attempts > 0:
        cell, backup = remove_single(board)
        removed += 1
        copy_board = Board(copy=board)
        solutions = 0
        solve_board(copy_board)
        if solutions != 1:
            board.fill_in(cell, backup)
            removed -= 1
            attempts -= 1
    return board


def export(board):
    f = open("Valid_sudoku.csv", "a")
    for i, cell in enumerate(board):
        f.write(str(cell))
        if i != 80:
            f.write(",")
    else:
        f.write("\n")
    f.close()


def set_initial_possible_numbers(board):
    for cell in board:
        for number in range(1, 10):
            if cell.number == 0 and number not in cell.possible_numbers:
                cell.possible_numbers.append(number)


def read_random_puzzles(filename, amount=1):
    f = open(filename, 'r')
    puzzles = f.read().splitlines()
    random_selection = []
    for i in range(amount):
        puzzle = puzzles[random.randint(0, len(puzzles) - 1)]
        puzzle = puzzle.split(',')
        board = Board(puzzle)
        random_selection.append(board)
    f.close()
    return random_selection

##for _ in range(1000):
#    start = time.perf_counter()
#    test = make_puzzle_symmetric(10)
#    export(test)
#    print(time.perf_counter() - start)

# test = read_random_puzzles("Valid_sudoku.csv")

##for x in test[0].get_square("C"):
#   print(x.square, x.row, x.column)
