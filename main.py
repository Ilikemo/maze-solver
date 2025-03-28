from window import Window
from classes import Point, Line
from maze import Maze
import time

def main():
    num_rows = 35
    num_cols = 45
    margin = 25
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    time.sleep(2)
    maze.solve()
    print("Done")

    win.wait_for_close()



main()