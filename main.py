from window import Window
from classes import Point, Line, Cell

def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(0, 0), Point(800, 600)), "black")
    cell1 = Cell(Point(1, 1), Point(20, 20), win)
    cell1.draw()
    cell2 = Cell(Point(200, 200), Point(300, 300), win, left_wall=False)
    cell2.draw()
    cell3 = Cell(Point(300, 300), Point(400, 400), win, top_wall=False)
    cell3.draw()
    cell2.draw_move(cell3)

    win.wait_for_close()



main()