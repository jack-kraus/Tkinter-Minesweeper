# Python Minesweeper Tkinter GUI Project

This is a small python GUI project of Minesweeper. It uses tkinter as a GUI framework. Follow instructions below to setup the project and play

## Setup

Download the directory and navigate to it. Make sure you have Python installed, and run the following command to install the dependency:

`pip install -r requirements.txt`

Then simply run `py run.py` for windows or `python3 run.py` for Mac or Linux

## Virtual Environment Setup

If you wish to run the game in a virtual environment, perform the following steps.
Download the directory and navigate to it. Make sure you have Python installed and are able to execute makefiles on your device. To setup the virtual environment, run:

`make setup`

To run the code after setting up, run:

`make run` 

To delete the virtual environment (note: this will require running setup again if you want to run)

`make clean`

## How to play

Start the game by selecting on the three difficulty levels: Easy, Medium, and Hard. Each subsequent level will increase the grid size and number of bombs.
Fastest times are saved below each diffuclty level and can be cleared with right click

![](https://i.imgur.com/nZsMI1S.png)

The game is played by trying to click cells to clear them without hitting bombs. The game can be played on Easy, Medium, or Hard, with each subsequent level
increasing the grid size and number of bombs. The number on a cell indicates how many cells in the surrounding cells in 8 directions are bombs, and cells with 0 surrounding bombs automatically clear out adjacent cells.
The first click is guaranteed to have 0 surrounding cells. Left click to clear and right click to "flag" a cell to indicate you think that there's a bomb there.
Flagged cells will not be cleared with a left click.

![](https://i.imgur.com/5DVugQj.png)

Once all of the non-bomb cells are cleared, you will win the game.
