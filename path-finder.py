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

        # reversed so DFS explores in desired order
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

                stdscr.addstr(i + 1, offset_x + j * 2, "X", PATH_COLOR)

            else:

                stdscr.addstr(i + 1, offset_x + j * 2, value, WALL_COLOR)


# ---------------- MAIN ----------------

def main(stdscr):

    curses.curs_set(0)

    curses.init_pair( 1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    bfs = bfs_search(maze)
    dfs = dfs_search(maze)

    bfs_done = False
    dfs_done = False

    bfs_path = []
    dfs_path = []

    bfs_start = time.time()
    dfs_start = time.time()

    bfs_end = None
    dfs_end = None

    while not (bfs_done and dfs_done):

        stdscr.clear()

        # -------- BFS --------

        if not bfs_done:

            try:
                bfs_path = next(bfs)

            except StopIteration:
                bfs_done = True
                bfs_end = time.time()

        # -------- DFS --------

        if not dfs_done:

            try:
                dfs_path = next(dfs)

            except StopIteration:
                dfs_done = True
                dfs_end = time.time()

        # -------- TIMERS --------

        bfs_elapsed = (
            bfs_end - bfs_start
            if bfs_end
            else time.time() - bfs_start
        )

        dfs_elapsed = (
            dfs_end - dfs_start
            if dfs_end
            else time.time() - dfs_start
        )

        # -------- DRAW BFS --------

        printMaze(maze, stdscr, bfs_path, offset_x=0, title="BFS", color=2)

        # -------- DRAW DFS --------

        printMaze(maze, stdscr, dfs_path, offset_x=35, title="DFS", color=3)

        # -------- DISPLAY TIMES --------

        stdscr.addstr(len(maze) + 3, 0, f"BFS Time: {bfs_elapsed:.2f} seconds")

        stdscr.addstr(len(maze) + 3, 35,f"DFS Time: {dfs_elapsed:.2f} seconds")

        stdscr.refresh()

        time.sleep(0.1)

    stdscr.getch()


wrapper(main)