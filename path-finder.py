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

# ---------------- BFS ----------------

def bfs_search(maze):

    start_pos = findStart(maze, "O")

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():

        current_pos, path = q.get()
        row, col = current_pos

        yield path

        if maze[row][col] == "X":
            return

        neighbors = findNeighbors(maze, row, col)

        for neighbor in neighbors:

            if neighbor in visited:
                continue

            r, c = neighbor

            if maze[r][c] == "#":
                continue

            visited.add(neighbor)

            new_path = path + [neighbor]

            q.put((neighbor, new_path))


# ---------------- DFS ----------------

def dfs_search(maze):

    start_pos = findStart(maze, "O")

    stack = [(start_pos, [start_pos])]

    visited = set()

    while stack:

        current_pos, path = stack.pop()
        row, col = current_pos

        if current_pos in visited:
            continue

        visited.add(current_pos)

        yield path

        if maze[row][col] == "X":
            return

        directions = [
            (-1, 0),  # up
            (0, 1),   # right
            (0, -1),  # left
            (1, 0)    # down
        ]

        for dr, dc in reversed(directions):

            new_row = row + dr
            new_col = col + dc

            if (
                0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[0])
                and maze[new_row][new_col] != "#"
            ):

                stack.append(
                    (
                        (new_row, new_col),
                        path + [(new_row, new_col)]
                    )
                )


# ---------------- HELPERS ----------------

def findStart(maze, start):

    for i, row in enumerate(maze):
        for j, value in enumerate(row):

            if value == start:
                return (i, j)

    return None


def findNeighbors(maze, row, col):

    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))

    if row + 1 < len(maze):
        neighbors.append((row + 1, col))

    if col > 0:
        neighbors.append((row, col - 1))

    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))

    return neighbors


# ---------------- DRAWING ----------------

def printMaze(maze, stdscr, path=[], offset_x=0, title="", color=2):

    WALL_COLOR = curses.color_pair(1)
    PATH_COLOR = curses.color_pair(color)

    stdscr.addstr(0, offset_x, title)

    for i, row in enumerate(maze):

        for j, value in enumerate(row):

            if (i, j) in path:

                stdscr.addstr(
                    i + 1,
                    offset_x + j * 2,
                    "X",
                    PATH_COLOR
                )

            else:

                stdscr.addstr(
                    i + 1,
                    offset_x + j * 2,
                    value,
                    WALL_COLOR
                )


# ---------------- MAIN ----------------

def main(stdscr):

    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    bfs = bfs_search(maze)
    dfs = dfs_search(maze)

    bfs_done = False
    dfs_done = False

    bfs_path = []
    dfs_path = []

    while not (bfs_done and dfs_done):

        stdscr.clear()

        if not bfs_done:

            try:
                bfs_path = next(bfs)

            except StopIteration:
                bfs_done = True

        if not dfs_done:

            try:
                dfs_path = next(dfs)

            except StopIteration:
                dfs_done = True

        # BFS on left
        printMaze(maze, stdscr, bfs_path, offset_x=0, title="BFS", color=2)

        # DFS on right
        printMaze(maze, stdscr, dfs_path, offset_x=35, title="DFS", color=3)

        stdscr.refresh()

        time.sleep(0.1)

    stdscr.getch()


wrapper(main)