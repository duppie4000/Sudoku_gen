from itertools import chain
from cell import *


def create_cell(i: int, j: int, number: int = 0):
    if i < 3:
        if j < 3:
            return Cell("A", i + 1, j + 1, number)
        elif j < 6:
            return Cell("B", i + 1, j + 1, number)
        else:
            return Cell("C", i + 1, j + 1, number)
    elif i < 6:
        if j < 3:
            return Cell("D", i + 1, j + 1, number)
        elif j < 6:
            return Cell("E", i + 1, j + 1, number)
        else:
            return Cell("F", i + 1, j + 1, number)
    else:
        if j < 3:
            return Cell("G", i + 1, j + 1, number)
        elif j < 6:
            return Cell("H", i + 1, j + 1, number)
        else:
            return Cell("I", i + 1, j + 1, number)


def convert(i, j, puzzle):
    return int(puzzle[(i * 9) + j])


class Board:
    def __init__(self, puzzle=None, copy=None, win=None):
        self.cells = []
        self.square_locs = {"A": (1, 1, 3, 3), "B": (1, 4, 3, 6), "C": (1, 7, 3, 9),
                            "D": (4, 1, 6, 3), "E": (4, 4, 6, 6), "F": (4, 7, 6, 9),
                            "G": (7, 1, 9, 3), "H": (7, 4, 9, 6), "I": (7, 7, 9, 9)}
        self.win = None
        if win:
            self.win = win

        if copy is None and puzzle is None:
            self.cells = [[create_cell(i, j) for j in range(9)] for i in range(9)]
            self.possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            self.number_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

        elif puzzle is not None and copy is None:
            self.cells = [[create_cell(i, j, convert(i, j, puzzle)) for j in range(9)] for i in range(9)]
            self.possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        else:
            self.cells = [[create_cell(i, j, copy.cells[i][j].number) for j in range(9)] for i in range(9)]
            self.possible_numbers = copy.possible_numbers

    def __repr__(self):
        count, count2 = 0, 0
        string = ""
        for x in self.cells:
            for y in x:
                if count == 0:
                    string += "|"
                string += str(y)
                count += 1
                if count == 3:
                    count = 0
                    string += "| "
            string += "\n"
            count2 += 1
            if count2 == 3:
                count2 = 0
                string += "\n"

        return string

    def __iter__(self):
        return (self.cells[i][j] for i in range(9) for j in range(9))

    def __hash__(self):
        numbers = []
        for x in self:
            numbers.append(str(x.possible_numbers))
            # numbers.append(str(x.number))
        return hash(str(numbers))

    def board_filled(self):
        for cell in self:
            if cell.number == 0:
                return False
        return True

    def possible_in_row(self, row, number):
        for cell in self.get_row(row):
            if cell.number == number:
                return False
        return True

    def possible_in_column(self, column, number):
        for cell in self.get_column(column):
            if cell.number == number:
                return False
        return True

    def possible_in_square(self, square, number):
        for cell in self.get_square(square):
            if cell.number == number:
                return False
        return True

    def possible(self, cell, number):
        return False if (not self.possible_in_row(cell.row, number) or
                         not self.possible_in_column(cell.column, number) or
                         not self.possible_in_square(cell.square, number)) else True

    def clear_all(self):
        for row in self.cells:
            for cell in row:
                self.clear_cell(cell)

    def fill_in(self, cell, number):
        cell.fill_in(number)
        if self.win:
            cell.draw(self.win)

    def clear_cell(self, cell=None, row=None, col=None):
        if not cell:
            self.cells[row - 1][col - 1].clear_cell()
        else:
            cell.clear_cell()
        if self.win:
            cell.draw(self.win)

    def get_cell(self, row, col):
        return self.cells[row - 1][col - 1]

    def remove_possible(self, cell, num):
        if cell.remove_possible(num):
            if self.win:
                cell.draw(self.win)

    def get_square(self, square):
        top = self.square_locs[square][0] - 1
        left = self.square_locs[square][1] - 1
        bottom = self.square_locs[square][2]
        right = self.square_locs[square][3]
        return (self.cells[i][j] for i in range(top, bottom) for j in range(left, right))

    def get_column(self, col):
        return (self.cells[i][col - 1] for i in range(9))

    def get_row(self, row):
        return (self.cells[row - 1][j] for j in range(9))

    def get_board_per_square(self):
        return chain(self.get_square("A"), self.get_square("B"), self.get_square("C"),
                     self.get_square("D"), self.get_square("E"), self.get_square("F"),
                     self.get_square("G"), self.get_square("H"), self.get_square("I"))

    def get_board_per_column(self):
        return chain(self.get_column(1), self.get_column(2), self.get_column(3), self.get_column(4), self.get_column(5),
                     self.get_column(6), self.get_column(7), self.get_column(8), self.get_column(9))

    def get_next_square(self, square):
        squares = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9}
        squares_inv = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'}
        square_number = squares[square] + 1
        if square_number == 10:
            raise LookupError("Square J does not exist")
        else:
            return self.get_square(squares_inv[square_number])

    def get_square_offset(self, square, up=0, down=0, left=0, right=0):
        squares = {'A': 0, 'B': 1, 'C': 2,'D': 3, 'E': 4, 'F': 5,'G': 6, 'H': 7, 'I': 8}
        squares_inv = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I'}
        translation = {(0, 0): 0, (0, 1): 0, (0, 2): 0,
                       (1, 0): 0, (1, 1): 0, (1, 2): -1,
                       (2, 0): 0, (2, 1): -2, (2, 2): -1}
        right = (right - left) % 3
        down = (down - up) % 3
        if right < 0:
            right += 3
        if down < 0:
            down += 3

        initial_square_num = squares[square]
        if translation[(initial_square_num % 3, right)] != 0:
            right = translation[(initial_square_num % 3, right)]
        if translation[(initial_square_num // 3, down)] != 0:
            down = translation[(initial_square_num % 3, down)]

        square_num = initial_square_num + right + (3 * down)
        return self.get_square(squares_inv[square_num])

    def draw(self):
        for cell in self:
            cell.draw(self.win)

    def undraw(self):
        for cell in self:
            cell.undraw()
