from .helpers import GameOutcome

class TicTacToe:
    P1 = "X"
    P2 = "O"
    BLANK = "_"

    def __init__(self, dim : int = 3):
        self.BLANK_BOARD : str = TicTacToe.BLANK * (dim * dim)  # generate blank board n x n board
        self.board : str = self.BLANK_BOARD
        self.dim : int = dim
        self.state : GameOutcome = GameOutcome.INCOMPLETE
        self.turn = 0 # whose turn is it

    def check_win(self):
        n = self.dim # board is n x n

        rows = [self.board[i * n : (i + 1) * n:] for i in range(n)] # get a list of rows
        columns = [self.board[i::n] for i in range(n)] # get a list of columns
        diagonals = [self.board[::n+1], self.board[n-1:n*n-1:n-1]] # get the two diagonals

        for length in rows + columns + diagonals:
            if length == TicTacToe.P1 * n:
                self.state = GameOutcome.P1_WON
                return
            elif length == TicTacToe.P2 * n:
                self.state = GameOutcome.P2_WON
                return

        self.state = GameOutcome.DRAW if self.board.count(TicTacToe.BLANK) == 0 else GameOutcome.INCOMPLETE

    def get_valid_moves(self):
        return [i for i in range(len(self.board)) if self.board[i] == TicTacToe.BLANK]

    # list of all blank indices
    def valid_moves(self, board=None):
        board = self.board if board is None else board
        return [i for i in range(self.dim ** 2) if board[i] == TicTacToe.BLANK]

    # make a move at the index
    def make_move(self, i):
        if self.is_over():
            raise Exception("Game is already over")

        inp_str = TicTacToe.P1 if self.turn == 0 else TicTacToe.P2
        if self.board[i] == TicTacToe.BLANK:
            self.board = self.board[:i] + inp_str + self.board[i+1:]
            self.turn = 1 if self.turn == 0 else 0 # invert turn
            return self.check_win()
        else:
            self.state = GameOutcome.P2_MISTAKE if self.turn == 1 else GameOutcome.P1_MISTAKE
            return self.state

    def reset_board(self):
        self.board = self.BLANK_BOARD
        self.state = GameOutcome.INCOMPLETE
        self.turn = 0

    # check if the game is over, i.e. the state is not incomplete
    def is_over(self):
        return self.state != GameOutcome.INCOMPLETE

    def __str__(self):
        n = self.dim # get width of board
        rows = [self.board[i * n : (i + 1) * n:] for i in range(n)] # get a list of rows
        row_strings = ["|".join(row) for row in rows] # get list of rows separated by "|"
        return "\n".join(row_strings) # return list of rows separated by newline