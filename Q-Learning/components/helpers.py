from enum import Enum

class GameOutcome(Enum):
    P1_WON = 0      # player one won
    DRAW = 1        # players got a draw
    P2_WON = 2      # player two won
    INCOMPLETE = 3  # game in progress
    P1_MISTAKE = 4  # player one tried to play on an occupied space
    P2_MISTAKE = 5  # player two tried to play on an occupied space

class Q_State(Enum):
    LEARN = 0   # Computer player is doing random moves to learn all outcomes
    WIN = 1     # Computer player is trying to win a game against a human

def print_progress(progress : float):
    print(f"{100 * progress}% done")