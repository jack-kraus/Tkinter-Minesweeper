import random
from enum import Enum
# declare

PLAYER = "X"
COMPUTER = "O"
BLANK = "-"
# BLANK_BOARD = BLANK * 9
TRIALS = 200000
SHOW_TRIAL = 750

class GameOutcome(Enum):
    LOSS = 0
    DRAW = 1
    WIN = 2
    INCOMPLETE = 3

class TicTacToe:
    PLAYER = "X"
    COMPUTER = "O"
    BLANK = "_"
    ROWS = 3
    COLUMNS = 3
    CH_REWARD = 10
    CH_PENALTY = -1000

    def __init__(self, dim : int = 3):
        self.BLANK_BOARD : str = TicTacToe.BLANK * (dim * dim)  # generate blank board n x n board
        self.board : str = self.BLANK_BOARD
        self.dim : int = dim

    def check_win(self):
        n = self.dim # board is n x n

        rows = [self.board[i * n : (i + 1) * n:] for i in range(n)] # get a list of rows
        columns = [self.board[i::n] for i in range(n)] # get a list of columns
        diagonals = [self.board[::n+1], self.board[n-1:n*n-1:n-1]] # get the two diagonals

        for length in rows + columns + diagonals:
            if length == TicTacToe.PLAYER * n:
                return GameOutcome.LOSS
            elif length == TicTacToe.COMPUTER * n:
                return GameOutcome.WIN

        return GameOutcome.DRAW if self.board.count(TicTacToe.BLANK) == 0 else GameOutcome.INCOMPLETE

    # list of all blank indices
    def valid_moves(self, board=None):
        board = self.board if board is None else board
        return [i for i in range(self.dim ** 2) if board[i] == TicTacToe.BLANK]

    # make a move at the index
    def make_move(self, i, inp_str):
        self.board = self.board[:i] + inp_str + self.board[i+1:]

    def reset_board(self):
        self.board = self.BLANK_BOARD

    def __str__(self):
        n = self.dim
        rows = [self.board[i * n : (i + 1) * n:] for i in range(n)] # get a list of rows
        row_strings = ["|".join(row) for row in rows]
        return "\n".join(row_strings)

print(TicTacToe())