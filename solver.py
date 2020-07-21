import time
from collections import deque
from itertools import combinations

from graphics import *

import puzzle

solve_path = deque()
marked = set()


def record_step(technique, operation, row, col, num):
    solve_path.append({"Technique": technique, "Operation": operation, "Row": row, "Column": col, "Number": num})


def format_solve():
    curr_technique = ""
    for step in solve_path:
        if curr_technique != step["Technique"]:
            print(step["Technique"], ": ")
            curr_technique = step["Technique"]
        print(step["Operation"], step["Number"], "in (", step["Row"], step["Column"], ")")


def set_possible_numbers(board):
    for cell in board:
        for number in range(1, 10):
            if cell.number == 0 and not board.possible(cell, number) and number in cell.possible_numbers:
                mark(cell, number, "Singles")
                remove_marked(board)
    remove_marked(board)


def singles(board):
    set_possible_numbers(board)
    filled = False
    for cell in board:
        if cell.number == 0:
            if len(cell.possible_numbers) == 1:
                board.fill_in(cell, cell.possible_numbers[0])
                record_step("Singles", "Filling", cell.row, cell.column, cell.number)
                filled = True
    return filled


def mark(cell, num, technique):
    marked.add((cell.row, cell.column, num))
    record_step(technique, "Marking", cell.row, cell.column, num)


def remove_marked(board):
    for move in marked:
        cell = board.get_cell(move[0], move[1])
        board.remove_possible(cell, move[2])
        record_step(solve_path[-1]["Technique"], "Removing", move[0], move[1], move[2])
    marked.clear()


def remove_possible_from_row(board, row, square, num, technique):
    removed = False
    for cell in board.get_row(row):
        if cell.square != square and num in cell.possible_numbers:
            mark(cell, num, technique)
            removed = True
    remove_marked(board)
    return removed


def remove_possible_from_column(board, column, square, num, technique):
    removed = False
    for cell in board.get_column(column):
        if cell.square != square and num in cell.possible_numbers:
            mark(cell, num, technique)
            removed = True
    remove_marked(board)
    return removed


def same_row(cells):
    test = cells[0].row
    for cell in cells:
        if cell.row != test:
            return False
    return True


def same_column(cells):
    test = cells[0].column
    for cell in cells:
        if cell.column != test:
            return False
    return True


def candidate_lines(board):
    for num in range(1, 10):
        seen = []
        for i, cell in enumerate(board.get_board_per_square(), start=1):
            if cell.number == 0 and num in cell.possible_numbers:
                seen.append(cell)
            if i % 9 == 0:
                if 4 > len(seen) > 1:
                    if same_row(seen) and remove_possible_from_row(board, seen[0].row, cell.square, num,
                                                                   "Candidate lines") or \
                            same_column(seen) and remove_possible_from_column(board, seen[0].column, cell.square, num,
                                                                              "Candidate lines"):
                        return True
                seen.clear()
    return False


# TODO Implement
def double_pairs(board):
    pass
    '''
    for num in range(1, 10):
        seen = {0: [], 1: [], 2: []}
        order = [{'right': (0, 1, 2), 'down': (0, 0, 0)}, {'right': (0, 1, 2), 'down': (1, 1, 1)},
                 {'right': (0, 1, 2), 'down': (2, 2, 2)},
                 {'right': (0, 0, 0), 'down': (0, 1, 2)}, {'right': (1, 1, 1), 'down': (0, 1, 2)},
                 {'right': (2, 2, 2), 'down': (0, 1, 2)}]
        for moves in order:
            for number in seen:
                right = moves['right'][number]
                down = moves['down'][number]
                seen[number] = find_candidate_in_square(board.get_square_offset('A', right=right, down=down), num)
            # seen[square] = find_candidate_in_square(board.get_square(square), num)
    # print(seen)
    '''


def find_candidate_in_square(cells, num):
    seen = []
    for cell in cells:
        if cell.number == 0 and num in cell.possible_numbers:
            seen.append(cell)
    if len(seen) == 2:
        return seen

    return []


def remove_possible_from_square(board, protected_cells, square, num, technique):
    removed = False
    for cell in board.get_square(square):
        if num in cell.possible_numbers and cell not in protected_cells:
            mark(cell, num, technique)
            removed = True

    return removed


def remove_impossible_from_cell(cell, protected_nums, technique):
    removed = False
    for num in cell.possible_numbers:
        if num not in protected_nums:
            mark(cell, num, technique)
            removed = True
    return removed


def naked_pairs(board):
    possible_pairs = set(combinations([1, 2, 3, 4, 5, 6, 7, 8, 9], 2))
    cells = []
    for pair in possible_pairs:
        for i, cell in enumerate(board.get_board_per_square(), start=1):
            if cell.number == 0 and len(cell.possible_numbers) == 2 and pair[0] in cell.possible_numbers \
                    and pair[1] in cell.possible_numbers:
                if not cells:
                    cells.append(cell)
                else:
                    if remove_possible_from_square(board, (cell, cells[0]), cell.square, pair[0], "Naked pairs") or \
                            remove_possible_from_square(board, (cell, cells[0]), cell.square, pair[1], "Naked pairs"):
                        remove_marked(board)
                        return True
            if i % 9 == 0:
                cells.clear()
    return False


def hidden_pairs(board, by="row"):
    possible_pairs = set(combinations([1, 2, 3, 4, 5, 6, 7, 8, 9], 2))
    cells = []
    skip = False
    for pair in possible_pairs:
        for i, cell in enumerate(board.get_board_per_square(), start=1):
            if cell.number == 0 and not skip:
                if (pair[0] in cell.possible_numbers and pair[1] not in cell.possible_numbers) or (
                        pair[0] not in cell.possible_numbers and pair[1] in cell.possible_numbers):
                    skip = True
                elif pair[0] in cell.possible_numbers and pair[1] in cell.possible_numbers:
                    cells.append(cell)

            if i % 9 == 0:
                if len(cells) == 2 and not skip:
                    if remove_impossible_from_cell(cells[0], pair, "Hidden pairs") or remove_impossible_from_cell(
                            cells[1], pair, "Hidden pairs"):
                        remove_marked(board)
                        return True
                skip = False
                cells.clear()
    return False


def hidden_singles(board):
    for num in range(1, 10):
        seen = []
        for i, cell in enumerate(board.get_board_per_square(), start=1):
            if cell.number == 0 and num in cell.possible_numbers:
                seen.append(cell)
            if i % 9 == 0:
                if len(seen) == 1:
                    temp = seen[0]
                    remove_impossible_from_cell(temp, [num], "Hidden singles")
                    remove_marked(board)
                    record_step("Hidden singles", "Filling", temp.row, temp.column, temp.number)
                    board.fill_in(temp, temp.number)
                    return True
                seen.clear()
    return False


def brute_force(board):
    cell = puzzle.empty_spot(board)
    if cell is None:
        return True

    for number in cell.possible_numbers:
        if board.possible(cell, number):
            board.fill_in(cell, number)
            if brute_force(board):
                return True
            board.clear_cell(cell)
    return False


def methods(board, method):
    if method == "Singles":
        return singles(board)
    elif method == "Hidden singles":
        return hidden_singles(board)
    elif method == "Candidate lines":
        return candidate_lines(board)
    elif method == "Naked pairs":
        return naked_pairs(board)
    elif method == "Hidden pairs":
        return hidden_pairs(board)
    elif method == "Double pairs":
        return double_pairs(board)
    else:
        raise Exception("Not a valid solving method")


def solve(board, win=None, techniques=None):
    puzzle.set_initial_possible_numbers(board)
    solve_path.clear()
    stats = {"Singles": 0, "Hidden singles": 0, "Candidate lines": 0, "Naked pairs": 0, "Hidden pairs": 0,
             "Double pairs": 0}
    if not techniques:
        techniques = ["Singles", "Hidden singles", "Candidate lines", "Naked pairs", "Hidden pairs", "Double pairs"]
    iterations = 0
    solved = True
    while not board.board_filled():
        iterations += 1
        for technique in techniques:
            if methods(board, technique):
                stats[technique] += 1
                break
        else:
            if not board.board_filled():
                remove_marked(board)
                print("No solution")
                if win:
                    win.getMouse()
                    board.win = None
                    brute_force(board)
                    board.win = win
                    board.draw()
                    time.sleep(3)
                solved = False
            break
    print(stats)
    return stats, solved


def square(x, y, size, win):
    p1 = Point(x, y)
    p2 = Point(x + size, y + size)
    rect = Rectangle(p1, p2)
    rect.setFill(color_rgb(255, 255, 255))
    rect.draw(win)


def make_window():
    win = GraphWin("Sudoku Solver", 480, 480)
    for x in range(0, 361, 160):
        for y in range(0, 361, 160):
            square(x, y, 160, win)
    return win
