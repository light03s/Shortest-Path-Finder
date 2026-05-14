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
    start_pos = findStart(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos])) # use a tuple to store the currentposition and the path to it in the list

    visited = set() # contains all visited positions

    while not q.empty():
        current_pos, path = q.get() # get the most recent element from the queue
        row, col = current_pos

        stdscr.clear()
        printMaze(maze, stdscr, path) # draw the path
        time.sleep(0.2) # make the iterations show up slower
        stdscr.refresh()

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

    # step 1: check for valid moves at the current node -> check in the order: up, right, left down
        # - can't go backwards
        # - can't go through a wall (#)
        # - can't go past the edges of the maze
    # step 2: place each visited node (current node) in the visited stack
    # step 3: if no possible options for traversal left, and the exit has not been reached, return false
    # step 4: go back through the visited nodes in the stack for the most recent node with unexplored neighboring options
        # mark the new node as traversed and repeat
    # step 5: when the end is reached return true through the succesful path to mark it


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
            if (i,j) in path:
                stdscr.addstr(i, j*3, "X", MAGENTA)
            else:
                stdscr.addstr(i, j*3, value, GREEN)


# function used to output onto terminal
def main(stdscr): 
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    
    findPath(maze, stdscr)
    stdscr.getch() # wait for user input something before exiting the program

wrapper(main) # this initializes the curses module
    