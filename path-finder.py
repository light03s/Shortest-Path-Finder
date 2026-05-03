import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "O", "#", "#"],
    ["#", "X", " ", " ", "#", " ", " ", " ", "#", " ", "#", "#"],
    ["#", "#", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", "#"],
    ["#", " ", "#", "#", "#", " ", "#", "#", "#", " ", "#", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", "#", " ", "#", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", "#", " ", "#", "#"],
    ["#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

# function used to output onto terminal
def main(stdscr): 
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
    color_theme = curses.color_pair(1)

    stdscr.clear()
    stdscr.addstr(10, 10, "Guten Tag!", color_theme) # when adding a astring need to add the position we are adding the string at
    stdscr.refresh()
    stdscr.getch() # wait for user input something before exiting the program

wrapper(main) # this initializes the curses module
    