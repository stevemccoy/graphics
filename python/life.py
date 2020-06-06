import numpy as np
import time
from graphics import GraphWin, Line, Point, Rectangle

class Life:

    # Background
    bgcolour = 'black'
    # For grid lines
    gridcolour = 'white'
    # For live cells
    cellcolour = 'blue'

    # Origin of grid    
    origin_x = 10
    origin_y = 10
    
    # Pixels per grid square.
    cell_height = 15
    cell_width = 15
    
    def __init__(self, width, height):
        self.nx = width
        self.ny = height
        self.aframe = np.zeros((self.nx,self.ny), dtype=np.uint8)
        self.bframe = np.zeros((self.nx,self.ny), dtype=np.uint8)
        self.iterations = 0
        self.win = self.create_window()

    def clear(self):
        self.clear_frame(self.aframe)
        self.clear_frame(self.bframe)
        self.iterations = 0

    def clear_frame(self, frame):
        for x in range(self.nx):
            for y in range(self.ny):
                frame[x][y] = 0

    # Move the image from the B frame (update) to the A frame (display)    
    def refresh_frames(self):
        for x in range(self.nx):
            for y in range(self.ny):
                self.aframe[x][y] = self.bframe[x][y]
    
    # Load an initial figure into the array, at the centre.
    def load(self, initial):
        (w,h) = np.shape(initial)
        startx = int((self.nx - w)/2)
        starty = int((self.ny - h)/2)
        if w < self.nx and h < self.ny:
            for x in range(w):
                for y in range(h):
                    self.bframe[startx + x][starty + y] = initial[x][y]

    def display(self):
        for y in range(self.ny):
            line = '|'
            for x in range(self.nx):
                if self.aframe[x][y] == 0:
                    line = line + ' '
                else:
                    line = line + '1'
            line = line + '|'
            print(line)
    
    # Look up if the given cell is alive (adjust for wrap around x and y coordinates).
    def is_cell_live(self, x, y):
        if x < 0:
            x += self.nx
        if x >= self.nx:
            x %= self.nx
        if y < 0:
            y += self.ny
        if y >= self.ny:
            y %= self.ny
        return self.aframe[x][y] != 0
                        
    # Determine how many neighbours of the given cell are alive.
    def neighbour_count(self, x, y):
        count = 0
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                if self.is_cell_live(x+dx, y+dy):
                    count += 1
        return count
    
    def create_window(self):
        initial_size = 500
        self.win = GraphWin("Conway's Game of Life", initial_size, initial_size)
        self.win.setBackground(self.bgcolour)
        return self.win
    
    # Draw the grid lines.
    def draw_grid(self):
    	total_height = self.origin_y + self.cell_height * self.ny
    	total_width = self.origin_x + self.cell_width * self.nx
    	for i in range(self.nx + 1):
    		x = self.origin_x + i * self.cell_width
    		l = Line(Point(x, self.origin_y), Point(x, total_height))
    		l.setOutline(self.gridcolour)
    		l.draw(self.win)
    	for i in range(self.ny + 1):
    		y = self.origin_y + i * self.cell_height
    		l = Line(Point(self.origin_x, y), Point(total_width, y))
    		l.setOutline(self.gridcolour)
    		l.draw(self.win)

    # Convert cell coordinates to graphical domain.
    def cell_coord(self, x, y):
        return (self.origin_x + self.cell_width * x, self.origin_y + self.cell_height * y)

    # Draw given cell in the given state.
    def draw_cell(self, x, y, state):
        (gx, gy) = self.cell_coord(x, y)
        inset = 1
        box = Rectangle(
            Point(gx + inset, gy + inset), 
            Point(gx + self.cell_width - inset, gy + self.cell_height - inset))
        box.setFill(self.bgcolour if state == 0 else self.cellcolour)
        box.draw(self.win)
        
    def render(self):
        for y in range(self.ny):
            for x in range(self.nx):
                self.draw_cell(x, y, self.aframe[x][y])
                
    def update_cells(self):
        for y in range(self.ny):
            for x in range(self.nx):
                count = self.neighbour_count(x, y)
                state = self.is_cell_live(x, y)
                new_state = state
                if state == 0 and count == 3:
                    new_state = 1
                    self.draw_cell(x, y, 1)
                elif state == 1 and (count < 2 or count > 3):
                    new_state = 0
                    self.draw_cell(x, y, 0)
                self.bframe[x][y] = new_state
        
def main():
    life = Life(30, 30)
    life.draw_grid()
    initialConfig = np.array([[1,1,1],[0,0,1],[0,1,0]])
    life.load(initialConfig)
    life.refresh_frames()
    life.render()
    
    while (True):
        life.update_cells()
        life.refresh_frames()
        time.sleep(0.1)
        
    
    life.win.getMouse()
    life.win.close()

main()



# game = Life(20,20)
# game.load(initialConfig)
# game.refresh_frames()
# game.display()





