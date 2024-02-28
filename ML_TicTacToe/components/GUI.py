from tkinter import *
from .Q_learner import Trainer

class GUI:
    def __init__(self, trials=1_000_000):
        # create window
        self.play_button_x, self.play_button_o = None, None
        self.window = Tk()
        self.window.title("Q-Learning TicTacToe")
        Label(self.window, text="Play TicTacToe", font="Helvetica 14 bold").pack()

        # define attributes
        self.ai = Trainer()
        self.trials = trials

        # check if app is closed
        self.app_closed = False

        # frame for moving buttons
        frame = Frame(self.window)
        frame.pack()

        # pack buttons into list
        self.buttons = []
        for i in range(9):
            new_button = Button(frame, width=7, text="X", height=2)
            new_button["state"] = "disabled"
            new_button["command"] = lambda n=i: self.player_move(n)
            new_button.grid(row = i//3, column = i%3)
            self.buttons.append(new_button)
        self.update_board()

        # label to show status
        self.label = Label(self.window, text="Play TicTacToe")
        self.label.pack()

        # start learning button
        self.button_grid = Frame(self.window)
        Button(self.button_grid, command=self.train_players, text="Train Agents").grid(row=0, column=0)
        self.button_grid.pack()

        # show learning progress
        self.canvas = Canvas(self.window, width=200, height=20, bg="white")
        self.canvas.pack()

        # main loop
        self.window.mainloop()

        # player going first or second
        self.human_p_num = 0

    def update_board(self):
        for i in range(9):
            self.buttons[i]["text"] = self.ai.game.board[i]

    def update_canvas(self, progress):
        width = float(self.canvas.cget('width'))
        height = float(self.canvas.cget('height'))
        self.canvas.create_rectangle(0, 0, progress * width, height, outline="green", fill="green")

    def set_button_state(self, state):
        for button in self.buttons:
            button["state"] = state

    def start_game(self, p_num : int = 0):
        self.set_button_state("normal")
        self.ai.start_test(p_num)
        self.update_board()
        self.label["text"] = ""

    def train_players(self):
        # destroy train button
        self.button_grid.winfo_children()[0].destroy()

        # update buttons
        self.play_button_x = Button(self.button_grid, command=lambda:self.start_game(0), text="Play as X", state="disabled")
        self.play_button_o = Button(self.button_grid, command=lambda: self.start_game(1), text="Play as O", state="disabled")
        self.play_button_x.grid(row=0, column=0)
        self.play_button_o.grid(row=0, column=1)

        # do training and get players
        self.ai.train(trials=self.trials, divisions=1_000, callback=self.update)
        self.ai.game.reset_board()

        # enable buttons
        self.play_button_x["state"] = "normal"
        self.play_button_o["state"] = "normal"

        # update the board to be blank
        self.update_board()

    # update event for training
    def update(self, progress):
        self.update_board()
        self.update_canvas(progress)
        self.window.update_idletasks()
        self.window.update()

    # what to do on close
    def on_close(self):
        self.app_closed = True

    def player_move(self, i):
        # error handling
        if i not in self.ai.game.get_valid_moves():
            self.label["text"] = "Try Again" if self.label["text"] != "Try Again" else "Invalid"
            return
        # else do a turn
        self.label["text"] = ""
        self.ai.player_move(i)
        self.update_board()
        if self.ai.game.is_over():
            self.label["text"] = str(self.ai.game.state)
            self.set_button_state("disabled")