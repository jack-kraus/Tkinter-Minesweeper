from .helpers import Q_State, GameOutcome, print_progress
import random
from .TicTacToe import TicTacToe
from typing import Callable
from .helpers import Q_State

class ComputerPlayer:
    def __init__(self):
        self.mode : Q_State = Q_State.LEARN
        self.Q : dict[str, list[int]] = {}
        self.last_move = None # board, choice

    # get move and save last move
    def get_move(self, game : TicTacToe, debug : bool = False):
        board = game.board
        q_entry: list[int] = self.get_q_entry(board)
        if self.mode == Q_State.LEARN:
            # if any not negative, choose randomly from those
            if any(reward > -1 for reward in q_entry):
                choices = [i for i in range(len(q_entry)) if q_entry[i] > -1]
            # else choose any
            else:
                choices = range(len(board))
        # if trying to win
        else:
            # get list of elements that are equal to the max reward of the action
            choices = [i for i in range(len(q_entry)) if q_entry[i] == max(q_entry)]
            if debug:
                print(q_entry)
                print(max(q_entry), choices)

        self.last_move = board, (choice := random.choice(choices))
        return choice

    # if game ends, reward based on outcome
    def reward(self, reward):
        # if no last move, nothing to learn from
        if self.last_move is None:
            return

        # unpack last move, get q entry
        board, choice = self.last_move
        q_entry : list[int] = self.get_q_entry(board)

        # if -1 reward, go to -1
        # if 0 reward, stay the same
        # if 1 reward, only go to 1 if current value is not negative
        match reward:
            case -1:
                q_entry[choice] = -1
            case 1:
                q_entry[choice] = 1 if 2 > q_entry[choice] > -1 else q_entry[choice]
            case 2:
                q_entry[choice] = 2 if q_entry[choice] > -1 else q_entry[choice]

    # if game in progress, reward based on new position rewards
    def learn(self, new_board : str):
        # if no last move, nothing to learn from
        if self.last_move is None:
            return

        # create (if nonexistent) q entry then return it
        new_rewards : list[int] = self.get_q_entry(new_board)

        # if all outcomes are negative, set this value to be negative
        if all(reward < 0 for reward in new_rewards):
            self.reward(-1)
        # if any outcome is positive, set this value to be positive
        elif any(reward > 0 for reward in new_rewards):
            self.reward(1)

    def get_q_entry(self, board):
        if board not in self.Q:
            self.Q[board] = [0] * len(board)
        return self.Q[board]

    def reset(self, state=Q_State.LEARN):
        self.last_move = None
        self.mode = state
        return self

class HumanPlayer:
    @staticmethod
    def get_move(game):
        board = game.board
        print(game)
        pos = [str(i) for i in range(len(board)) if board[i] == TicTacToe.BLANK]
        while (move := input("Move: ")).strip() not in pos:
            print("Incorrect; try again")
        return int(move.strip())

class Trainer:
    def __init__(self, dim : int = 3):
        self.human_p_num = 0
        self.game = TicTacToe(dim)
        self.p1, self.p2 = ComputerPlayer(), ComputerPlayer()
        self.mode : Q_State = Q_State.LEARN

    def train_game(self):
        self.game.reset_board()
        self.p1.reset(Q_State.LEARN)
        self.p2.reset(Q_State.LEARN)

        while self.game.state == GameOutcome.INCOMPLETE:
            p1_move = self.p1.get_move(self.game)
            self.game.make_move(p1_move)
            self.p2.learn(self.game.board)
            # print(self.game, end=f"\nX move at {p1_move}\n\n")

            # break if game over
            if self.game.state != GameOutcome.INCOMPLETE:
                break

            p2_move = self.p2.get_move(self.game)
            self.game.make_move(p2_move)
            self.p1.learn(self.game.board)
            # print(self.game, end=f"\nO move at {p2_move}\n\n")

        match self.game.state:
            case GameOutcome.P1_WON:
                self.p1.reward(2)
                self.p2.reward(-1)
            case GameOutcome.P2_WON:
                self.p1.reward(-1)
                self.p2.reward(2)
            case GameOutcome.P1_MISTAKE:
                self.p1.reward(-1)
            case GameOutcome.P2_MISTAKE:
                self.p2.reward(-1)

        return self.game.board

    def train(self, trials : int = 1_000_000, divisions : int = 10, callback : Callable[[float], None] = print_progress):
        for i in range(trials):
            self.train_game()
            if (i+1) % (trials // divisions) == 0:
                callback((i+1) / trials)
        self.mode = Q_State.WIN

    def test_game(self, human_p_num=0):
        p1 = self.p1.reset(Q_State.WIN) if human_p_num == 1 else HumanPlayer()
        p2 = self.p2.reset(Q_State.WIN) if human_p_num == 0 else HumanPlayer()
        self.game.reset_board()

        while self.game.state == GameOutcome.INCOMPLETE:
            p1_move = p1.get_move(self.game)
            self.game.make_move(p1_move)

            # break if game over
            if self.game.state != GameOutcome.INCOMPLETE:
                break

            p2_move = p2.get_move(self.game)
            self.game.make_move(p2_move)
        print(self.game)
        print(self.game.state)

    def start_test(self, p_num : int = 0):
        # reset components
        self.p1.reset(Q_State.WIN)
        self.p2.reset(Q_State.WIN)
        self.game.reset_board()

        # start conditions
        self.human_p_num = p_num
        if p_num == 1:
            self.game.make_move(self.p1.get_move(self.game, debug=True))

    def player_move(self, i : int = 0):
        self.game.make_move(i)
        if not self.game.is_over():
            other = self.p2 if self.human_p_num == 0 else self.p1
            self.game.make_move(other.get_move(self.game, debug=True))