import puzzle
import solver


def write_out(filename, line):
    f = open(filename, 'a')
    f.write(line)
    f.write("\n")
    f.close()


def read(filename):
    f = open(filename, 'r')
    sudokus = f.read().splitlines()
    f.close()
    return sudokus


def super_easy_puzzles(filename):
    sudokus = read(filename)
    for line in sudokus:
        sudoku = line.split(',')
        stats, solved = solver.solve(puzzle.Board(sudoku))
        if solved and stats['Candidate lines'] == 0 and stats['Naked pairs'] == 0 and stats['Hidden pairs'] == 0:
            write_out("super_easy.csv", line)
        else:
            write_out("not_super_easy.csv", line)


super_easy_puzzles("not_super_easy.csv")
