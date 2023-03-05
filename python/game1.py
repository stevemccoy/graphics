import pygame as pg
import numpy as np


# Globals.
screen_width = screen_height = 630
margin_px = 15
cell_size_px = 10

num_cols = (screen_width - margin_px * 2) // cell_size_px
num_rows = (screen_height - margin_px * 2) // cell_size_px

back_color = "purple"
grid_color = (128, 128, 128)

live_color = (255, 255, 255)
dead_color = (0, 0, 0)

# Background and foreground frames.
bg = np.random.randint(2, size=(num_rows, num_cols))
fg = np.copy(bg)


# Functions.
def draw_grid():
    for x in range(margin_px, screen_width - margin_px + 1, cell_size_px):
        pg.draw.line(screen, grid_color, (x, margin_px), (x, screen_height - margin_px))
    for y in range(margin_px, screen_height - margin_px + 1, cell_size_px):
        pg.draw.line(screen, grid_color, (margin_px, y), (screen_width - margin_px, y))

def draw_cell(col, row):
    color = live_color if fg[row, col] else dead_color
    gx = margin_px + col * cell_size_px
    gy = margin_px + row * cell_size_px
    pg.draw.rect(screen, color, (gx + 1, gy + 1, cell_size_px - 2, cell_size_px - 2))

def refresh_whole_grid():
    for y in range(num_rows):
        for x in range(num_cols):
            draw_cell(x, y)

def update_cell(col, row):
    cell = bg[col][row]
    x1, y1 = max(col - 1, 0), max(row - 1, 0)
    x2, y2 = min(col + 2, num_cols), min(row + 2, num_rows)
    count = sum(sum(bg[x1:x2, y1:y2])) - cell
    if cell:
        if count < 2 or count > 3:
            fg[col][row] = 0
            return True
    else:
        if count == 3:
            fg[col][row] = 1
            return True
    return False

def update_frame():
    bg = np.copy(fg)
    for y in range(num_rows):
        for x in range(num_cols):
            if update_cell(x, y):
                draw_cell(x, y)

# Initialise and run.
pg.init()
screen = pg.display.set_mode((screen_width,screen_height))
clock = pg.time.Clock()

screen.fill(back_color)  # Fill the display with a solid color
draw_grid()
refresh_whole_grid()

while True:
    # Process player inputs.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

    # Do logical updates here.
    # ...
    update_frame()

#    r = pg.draw.rect(screen, grid_color, (100,100,100,100) )
#    screen.update()

    # Render the graphics here.
    # ...

    pg.display.flip()  # Refresh on-screen display
#    clock.tick(60)         # wait until next frame (at 60 FPS)
