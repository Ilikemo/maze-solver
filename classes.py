from tkinter import Tk, BOTH, Canvas
import time
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color)

class Cell:
    def __init__(self, top_left_point, bottom_right_point, window = None, left_wall=True, top_wall=True, right_wall=True, bottom_wall=True):
        self.has_left_wall = left_wall
        self.has_top_wall = top_wall
        self.has_right_wall = right_wall
        self.has_bottom_wall = bottom_wall
        self._top_left = top_left_point
        self._bottom_right = bottom_right_point
        self._win = window
        self.visited = False

    def draw(self):
        self._top_right = Point(self._bottom_right.x, self._top_left.y)
        self._bottom_left = Point(self._top_left.x, self._bottom_right.y)
        if self._win is None:
            return
        if self.has_left_wall:
            self._win.draw_line(Line(self._top_left, self._bottom_left), "black")
        else:
            self._win.draw_line(Line(self._top_left, self._bottom_left), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(self._top_left, self._top_right), "black")
        else:
            self._win.draw_line(Line(self._top_left, self._top_right), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(self._top_right, self._bottom_right), "black")
        else:
             self._win.draw_line(Line(self._top_right, self._bottom_right), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(self._bottom_left, self._bottom_right), "black")
        else:
            self._win.draw_line(Line(self._bottom_left, self._bottom_right), "white")

    def draw_move(self, to_cell, undo=False):
        self._center_point = Point((self._top_left.x + self._bottom_right.x) / 2, (self._top_left.y + self._bottom_right.y) / 2)
        if undo is False:
            color = "red"
        else:
            color = "gray"
        self._win.draw_line(Line(self._center_point, to_cell._center_point), color)
        
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._x1 = x1       # top left corner of the maze
        self._y1 = y1       # top left corner of the maze
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is None:
            random.seed(seed)
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visted()
    
    def _create_cells(self):
        tmp_x = self._x1
        tmp_y = self._y1
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                cell = Cell(Point(0, 0), Point(0, 0), self._win)    # creates a cell and calculates it's coordinates later in the _draw_cell method
                column.append(cell)
            self._cells.append(column)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
            x = self._x1 + i * self._cell_size_x
            y = self._y1 + j * self._cell_size_y
            top_left = Point(x, y)
            bottom_right = Point(x + self._cell_size_x, y + self._cell_size_y)
            self._cells[i][j]._top_left = top_left
            self._cells[i][j]._bottom_right = bottom_right
            self._cells[i][j].draw()
            self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[0][0].draw()
        self._cells[-1][-1].has_bottom_wall = False
        self._cells[-1][-1].draw()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            neighbors = {}
            if i > 0 and not self._cells[i - 1][j].visited:
                neighbors["up"] = (i - 1, j)
            if j > 0 and not self._cells[i][j - 1].visited:
                neighbors["left"] = (i, j - 1)
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                neighbors["right"] = (i + 1, j)
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                neighbors["down"] = (i, j + 1)
            if len(neighbors) == 0:
                self._cells[i][j].draw()
                return
            direction = random.choice(list(neighbors.keys()))
            next_i, next_j = neighbors[direction]
            if direction == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            if direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            if direction == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            self._cells[i][j].draw()
            self._cells[next_i][next_j].draw()
            self._break_walls_r(next_i, next_j)

    