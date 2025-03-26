import time
import random
from classes import Cell, Point


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._x1 = x1       # top left corner of the maze
        self._y1 = y1       # top left corner of the maze
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
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
        time.sleep(0.0001)

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
                neighbors["left"] = (i - 1, j)
            if j > 0 and not self._cells[i][j - 1].visited:
                neighbors["up"] = (i, j - 1)
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
            self._animate()
            self._break_walls_r(next_i, next_j)


    def _reset_cells_visted(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        directions = []
        if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i + 1][j].visited:
            directions.append("right")
        if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j + 1].visited:
            directions.append("down")
        if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j - 1].visited:
            directions.append("up")
        if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i - 1][j].visited:
            directions.append("left")
        
        
        if len(directions) == 0:
            return False
        for direction in directions:
            if direction == "left":
                self._cells[i][j].draw_move(self._cells[i - 1][j])
                if self._solve_r(i - 1, j):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)
            if direction == "up":
                self._cells[i][j].draw_move(self._cells[i][j - 1])
                if self._solve_r(i, j - 1):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)
            if direction == "right":
                self._cells[i][j].draw_move(self._cells[i + 1][j])
                if self._solve_r(i + 1, j):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True) 
            if direction == "down":
                self._cells[i][j].draw_move(self._cells[i][j + 1])
                if self._solve_r(i, j + 1):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)
        return False
            
