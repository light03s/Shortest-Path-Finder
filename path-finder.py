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

# breadth-first search - gaurunteed to find a solution
def findPath(maze, stdscr):
    start = "O"
    end = "X"

    q = queue.Queue()
    q.put((start_pos, [start_pos])) # use a tuple to store the currentposition and the path to it in the list

    visited = set() # contains all visited positions

    while not q.empty():
        current_pos, path = q.get() # get the most recent element from the queue
        row, col = current_pos

        if maze[row][col] == end:
            return path
        
    # if we have not reached the end then we check for neighbors
    neighbors = findNeighbors(maze, row, col)
    for neighbor in neighbors:
        if neighbor in visited: # do not process spaces that are already visited
            continue
        
        r, c = neighbor
        if maze[r][c] == "#": # not not process #
            continue
        
        # if the neighbor is not visited and is not a # add it to the path and add it to the queue
        new_path = path + [neighbor]
        q.put((neighbor, new_path))
        visited.add(neighbor)

# depth-first search - gaurunteed to find a solution

# find the coordinates of the initial position
def findStart(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i,j # return the position of O
            
    return None # when position does not = O

def findNeighbors(maze, row, col): # make sure the neighbors are a valid next position in the maze
    neighbors = []

    if row > 0: # go up
        neighbors.append((row - 1, col))
    if row + 1 < len(maze): # go down
        neighbors.append((row + 1, col))
    if col > 0: # go left
        neighbors.append((row, col - 1 ))
    if col + 1 < len(maze[0]): # go right
        neighbors.append((row, col + 1 ))

    return neighbors

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
    