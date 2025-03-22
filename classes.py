from tkinter import Tk, BOTH, Canvas


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
        _top_right = Point(self._bottom_right.x, self._top_left.y)
        _bottom_left = Point(self._top_left.x, self._bottom_right.y)
        if self._win is None:
            return
        if self.has_left_wall:
            self._win.draw_line(Line(self._top_left, _bottom_left), "black")
        else:
            self._win.draw_line(Line(self._top_left, _bottom_left), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(self._top_left, _top_right), "black")
        else:
            self._win.draw_line(Line(self._top_left, _top_right), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(_top_right, self._bottom_right), "black")
        else:
             self._win.draw_line(Line(_top_right, self._bottom_right), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(_bottom_left, self._bottom_right), "black")
        else:
            self._win.draw_line(Line(_bottom_left, self._bottom_right), "white")

    def draw_move(self, to_cell, undo=False):
        self._center_point = Point((self._top_left.x + self._bottom_right.x) / 2, (self._top_left.y + self._bottom_right.y) / 2)
        to_cell._center_point = Point((to_cell._top_left.x + to_cell._bottom_right.x) / 2, (to_cell._top_left.y + to_cell._bottom_right.y) / 2)
        if undo is False:
            color = "red"
        else:
            color = "gray"
        self._win.draw_line(Line(self._center_point, to_cell._center_point), color)
        
