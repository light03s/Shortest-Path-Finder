import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "X", "#", "#", "#", "#", "#", "O", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", "#", "#", " ", "#", " ", "#"],
    ["#", " ", " ", "#", " ", " ", " ", " ", "#"],
    ["#", "#", " ", "#", " ", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

def printMaze(maze, stdscr, path=[]):
    GREEN = curses.color_pair(1)
    MAGENTA = curses.color_pair(2)

    for i, row in enumerate(maze): # enumerate returns the index and value in the maze
        for j, value in enumerate(row):
            stdscr.addstr(i, j*3, value, GREEN)


# function used to output onto terminal
def main(stdscr): 
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    color_theme = curses.color_pair(1)

    stdscr.clear()
    printMaze(maze, stdscr)
    stdscr.refresh()
    stdscr.getch() # wait for user input something before exiting the program

wrapper(main) # this initializes the curses module
    