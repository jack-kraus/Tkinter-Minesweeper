from enum import Enum
import os
import time
import json
class MinesweeperStates(Enum):
    INACTIVE = 0 # before starting
    ACTIVE = 1 # in gameplay
    WON = 2 # won the game
    LOST = 3 # hit a mine
    QUIT = 4 # quitting the game

class Stopwatch:
    def __init__(self):
        self.__start_time = time.time()
        self.__end_time = time.time()

    def start(self):
        self.__start_time = time.time()

    def stop(self):
        self.__end_time = time.time()

    def reset(self):
        self.__start_time = time.time()
        self.__end_time = time.time()

    def get_elapsed_time(self):
        return round(self.__end_time - self.__start_time, 2)

def create_high_scores():
    if not os.path.exists("highscores.json"):
        dictionary = {"easy": -1, "medium": -1, "hard": -1}
        with open("highscores.json", "w") as outfile:
            json.dump(dictionary, outfile)

def set_high_score(mode, value):
    create_high_scores()
    with open("highscores.json", 'r') as openfile:
        dictionary = json.load(openfile)
    with open("highscores.json", 'w') as outfile:
        dictionary[mode] = value
        json.dump(dictionary, outfile)

def get_high_score(mode):
    create_high_scores()
    with open("highscores.json", 'r') as openfile:
        json_object = json.load(openfile)
        return json_object[mode]

def reset_high_score(mode):
    set_high_score(mode, -1)