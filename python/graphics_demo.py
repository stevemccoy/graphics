
from graphics import *

def grid(win, nx, ny, w, h):
	ox = 10
	oy = 10
	total_height = oy + h * ny
	total_width = ox + w * nx
	for i in range(nx + 1):
		x = ox + i * w
		l = Line(Point(x, oy), Point(x, total_height))
		l.setOutline('black')
		l.draw(win)
	for i in range(ny + 1):
		y = oy + i * h
		l = Line(Point(ox, y), Point(total_width, y))
		l.setOutline('black')
		l.draw(win)


def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground('pink')

	grid(win, 10, 10, 40, 40)


	win.getMouse()
	win.close()

main()
