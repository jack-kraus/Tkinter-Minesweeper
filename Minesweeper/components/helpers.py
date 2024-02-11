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

def set_high_score(mode, value):
    if not os.path.exists("highscores.json"):
        dictionary = {"easy": -1, "medium": -1, "hard": -1}
    else:
        with open("highscores.json", 'r') as openfile:
            dictionary = json.load(openfile)
    dictionary[mode] = value
    with open("highscores.json", "w") as outfile:
        json.dump(dictionary, outfile)

def get_high_score(mode):
    if not os.path.exists("highscores.json"):
        dictionary = { "easy" : -1, "medium": -1, "hard": -1 }
        with open("highscores.json", "w") as outfile:
            json.dump(dictionary, outfile)
        return -1
    else:
        with open("highscores.json", 'r') as openfile:
            json_object = json.load(openfile)
            return json_object[mode]