from graphics import *


class Cell:
    def __init__(self, square: str, row: int, column: int, number: int = 0):
        self.number = number
        self.notes = []
        self.editable = True
        self.square = square
        self.row = row
        self.column = column
        self.possible_numbers = []
        self.loc = Point((self.column - 1) * 53 + 28, (self.row - 1) * 53 + 28)
        self.text = Text(self.loc, number)
        self.text.setSize(20)
        row_loc = (self.column - 1) * 53
        col_loc = (self.row - 1) * 53
        self.possible_locs = [
            Point(row_loc + 14, col_loc + 14), Point(row_loc + 28, col_loc + 14), Point(row_loc + 42, col_loc + 14),
            Point(row_loc + 14, col_loc + 28), Point(row_loc + 28, col_loc + 28), Point(row_loc + 42, col_loc + 28),
            Point(row_loc + 14, col_loc + 42), Point(row_loc + 28, col_loc + 42), Point(row_loc + 42, col_loc + 42)]
        self.possible_text = [Text(self.possible_locs[x], x + 1) for x in range(len(self.possible_locs))]

    def __repr__(self):
        return str(self.number)

    def add_note(self, number: int):
        if number not in self.notes:
            self.notes.append(number)
        else:
            self.notes.remove(number)

    def fill_in(self, number: int):
        if self.editable and self.number != number:
            self.number = number
            self.text.setText(self.number)

    def clear_cell(self):
        if self.editable:
            self.notes = []
            self.number = 0
            self.text.setText(0)

    def remove_possible(self, num):
        if num in self.possible_numbers:
            self.possible_numbers.remove(num)
            if not self.possible_numbers:
                print("Help, I'm empty")
            return True
        return False

    def add_possible(self, num):
        if num not in self.possible_numbers:
            self.possible_numbers.append(num)

    def draw(self, win):
        self.undraw()
        if self.number != 0:
            self.text.draw(win)
        else:
            for num in self.possible_text:
                if num.getText() in self.possible_numbers:
                    num.draw(win)

    def undraw(self):
        self.text.undraw()
        for num in self.possible_text:
            num.undraw()
