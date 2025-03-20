from tkinter import Tk, BOTH, Canvas
from classes import Point, Line




class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__width = width
        self.__height = height
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=self.__width, height=self.__height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        
    def close(self):
        self.__running = False
        
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)