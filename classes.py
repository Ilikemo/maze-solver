from tkinter import Tk, BOTH, Canvas
import time

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
        
        self._center_point = Point((self._top_left.x + self._bottom_right.x) / 2, (self._top_left.y + self._bottom_right.y) / 2) # center point of the cell used to draw moves
        self._win = window

    def draw(self):
        self._top_right = Point(self._bottom_right.x, self._top_left.y)
        self._bottom_left = Point(self._top_left.x, self._bottom_right.y)
        if self._win is None:
            return
        if self.has_left_wall:
            self._win.draw_line(Line(self._top_left, self._bottom_left), "black")
        if self.has_top_wall:
            self._win.draw_line(Line(self._top_left, self._top_right), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(self._top_right, self._bottom_right), "black")
        if self.has_bottom_wall:
            self._win.draw_line(Line(self._bottom_left, self._bottom_right), "black")

    def draw_move(self, to_cell, undo=False):
        if undo is False:
            color = "red"
        else:
            color = "gray"
        self._win.draw_line(Line(self._center_point, to_cell._center_point), color)
        
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None):
        self._x1 = x1       # top left corner of the maze
        self._y1 = y1       # top left corner of the maze
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
    
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
        self._win.redraw()
        time.sleep(0.05)


