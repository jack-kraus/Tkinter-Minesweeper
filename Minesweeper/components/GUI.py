from tkinter import *  # Import all definitions from tkinter
from components.helpers import MinesweeperStates as States
from components.helpers import get_high_score, set_high_score, Stopwatch
from components.CellButton import CellButton
import random
from itertools import product
from functools import reduce
from tkinter import Frame

class Minesweeper:
    def __init__(self, columns=10, rows=10, bombs=10, mode=""):
        self.state = States.INACTIVE
        self.shape = (rows, columns)
        self.board = -1
        self.bombs = bombs
        self.stopwatch = Stopwatch()
        self.mode = mode

        # set up window
        self.window = Tk()
        self.window.title("Minesweeper")
        self.time = StringVar(value="Hello")

        main_frame= Frame(self.window)
        main_frame.pack()

        self.status_label = Label(main_frame, text="Minesweeper", font="Helvetica 14 bold")
        self.status_label.pack(padx=10, pady=10)

        grid_frame = Frame(main_frame)
        grid_frame.pack(padx=10)

        self.time_label = Label(main_frame, text="Time: 0")
        self.time_label.pack()

        button_frame = Frame(main_frame)
        button_frame.pack()
        Button(button_frame, text="Play Again", command=self.reset, fg="white", bg="gray").pack(side=LEFT, padx=10, pady=10)
        Button(button_frame, text="Return to Menu", command=self.return_to_menu, fg="white", bg="gray").pack(side=LEFT, padx=10, pady=10)
        self.update_time_label()
        # generate 2d array of buttons
        self.buttons = [[CellButton(grid_frame, self.hit_button, ir, ic) for ic in range(columns)] for ir in range(rows)]
        self.window.mainloop()

    def generate_board(self, r, c):
        bombs = self.bombs
        rows, columns = self.shape # get rows and columns
        self.board = [[0 for _ in range(columns)] for _ in range(rows)] # starting array full of zeroes
        while bombs > 0:
            rr, rc = random.randrange(0, rows), random.randrange(0, columns) # random coordinate
            # if not already a bomb, and not adjacent to the starting click
            if self.board[rr][rc] != -1 and (rr - r) ** 2 + (rc - c) ** 2 > 2:
                self.board[rr][rc] = -1 # set to bomb
                bombs -= 1
        for r in range(rows):
            for c in range(columns):
                if self.board[r][c] != -1:
                    # convert coordinates to values of the grid
                    surrounding_vals = map(lambda i: self.board[i[0]][i[1]], self.surrounding(r, c))
                    # set board to number of surrounding bombs (-1 values)
                    self.board[r][c] = len(list(filter(lambda i : i == -1, surrounding_vals)))

    # get list of vertices adjacent a point
    def surrounding(self, r, c):
        rows, columns = self.shape # get rows and columns
        v_rows = [i for i in range(max(0, r - 1), min(r + 2, rows))] # all rows adjacent in grid
        v_columns = [i for i in range(max(0, c - 1), min(c + 2, columns))] # all columns adjacent in grid
        v_coordinates = list(product(v_rows, v_columns)) # list of all combinations of the two lists
        v_coordinates.remove((r, c)) # remove current item
        return v_coordinates

    def hit_button(self, _, r, c):
        if self.state == States.INACTIVE:
            self.generate_board(r, c)
            self.state = States.ACTIVE
            self.stopwatch.start()
        elif self.state != States.ACTIVE: return
        button, cell_value = self.buttons[r][c], self.board[r][c]
        # if hit unsuccessful or cell value is not 0, the call is over
        if not button.hit(cell_value): return
        elif cell_value == -1:
            self.end_game(States.LOST)
            return
        elif self.check_win():
            self.end_game(States.WON)
            return
        elif cell_value != 0: return
        # else iterate over adjacent tiles
        for adj_cell in self.surrounding(r, c):
            ar, ac = adj_cell
            self.hit_button(_, ar, ac)  # hit all adjacent buttons

    # disable all buttons in case of win or loss
    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.disable()

    def end_game(self, state):
        self.state = state
        self.stopwatch.stop()
        self.disable_buttons()
        self.status_label["text"] = "You Won!" if state == States.WON else "Game Over"
        # update high score
        if self.state == States.WON and self.mode != "":
            new_score = self.stopwatch.get_elapsed_time()
            old_score = get_high_score(self.mode)
            if old_score == -1 or new_score < old_score:
                set_high_score(self.mode, new_score)

    def check_win(self):
        # for each row of buttons, convert it to the number of buttons that have been revealed
        revealed = [reduce(lambda a, b: a + b, map(lambda r: r.revealed, row) ) for row in self.buttons]
        # we won if the amount revealed equals total cells minus bombs
        return sum(revealed) == self.shape[0] * self.shape[1] - self.bombs

    def reset(self):
        self.state = States.INACTIVE
        self.board = -1
        self.status_label["text"] = "Minesweeper"
        self.stopwatch.reset()
        for row in self.buttons:
            for button in row:
                button.reset()

    def update_time_label(self):
        if self.state == States.ACTIVE: self.stopwatch.stop()
        self.time_label["text"] = f"Time: {self.stopwatch.get_elapsed_time()}"
        if self.state == States.QUIT:
            self.window.destroy()
        else:
            self.window.after(100, self.update_time_label)

    def return_to_menu(self):
        self.state = States.QUIT
        ModeSelect()

    def __str__(self):
        return "\n".join(map(str, self.board))

class ModeSelect:
    def __init__(self):
        self.window = Tk()
        self.window.title("Minesweeper")

        text1 = Label(self.window, text="Minesweeper", font="Helvetica 14 bold")
        text1.pack(pady=10)
        frame = Frame(self.window)
        frame.pack(padx=20, pady=10)
        easy = Button(frame, text="Easy", command=self.easy, width=10, fg="white", bg="gray")
        medium = Button(frame, text="Medium", command=self.medium, width=10, fg="white", bg="gray")
        hard = Button(frame, text="Hard", command=self.hard, width=10, fg="white", bg="gray")
        easy.grid(row=1, column=1)
        medium.grid(row=1, column=2)
        hard.grid(row=1, column=3)

        Label(frame, text="Highscores", width=10, font="Helvetica 10 bold").grid(row=2, column=2, padx=5, pady=5)

        highscores = [ get_high_score("easy"), get_high_score("medium"), get_high_score("hard") ]
        easy_label = Label(frame, text=str(highscores[0]) if highscores[0] != -1 else "None", width=10, relief=SUNKEN)
        medium_label = Label(frame, text=str(highscores[1]) if highscores[1] != -1 else "None", width=10, relief=SUNKEN)
        hard_label = Label(frame, text=str(highscores[2]) if highscores[2] != -1 else "None", width=10, relief=SUNKEN)
        easy_label.grid(row=3, column=1)
        medium_label.grid(row=3, column=2)
        hard_label.grid(row=3, column=3)

        self.window.mainloop()

    def easy(self):
        self.window.destroy()
        Minesweeper(10, 8, 10, "easy")

    def medium(self):
        self.window.destroy()
        Minesweeper(18, 14, 40, "medium")

    def hard(self):
        self.window.destroy()
        Minesweeper(24, 20, 99, "hard")

ModeSelect()