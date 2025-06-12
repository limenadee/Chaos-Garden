import pygame
import numpy as np
import random

sizeOfCell = 10
width = 1600
height = 1000
row = height // sizeOfCell
column = width // sizeOfCell

# color section
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
initOptions = [BLUE, RED, GREEN]

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("chaos garden attempt")
clock = pygame.time.Clock()
paused = True
mouse_down = False

# initializing the grids
logic_grid = np.random.randint(2, size=(row, column), dtype=np.uint8)

color_grid = np.empty((row, column), dtype=object)
for y in range(row):
    for x in range(column):
        if logic_grid[y, x] == 1:
            color_grid[y, x] = random.choice(initOptions)
        else:
            color_grid[y, x] = BLACK  # or None

def redo_grid():
    global logic_grid, color_grid
    logic_grid = np.random.randint(2, size=(row, column), dtype=np.uint8)
    color_grid = np.empty((row, column), dtype=object)
    for y in range(row):
        for x in range(column):
            if logic_grid[y, x] == 1:
                color_grid[y, x] = random.choice(initOptions)
            else:
                color_grid[y, x] = BLACK

def refresh_grid():
    global logic_grid, color_grid
    logic_grid = np.empty((row, column), dtype=np.uint8)
    color_grid = np.empty((row, column), dtype=object)
    for y in range(row):
        for x in range(column):
            if logic_grid[y, x] == 1:
                color_grid[y, x] = random.choice(initOptions)
            else:
                color_grid[y, x] = BLACK

color_grid = np.empty((row, column), dtype=object)
for y in range(row):
    for x in range(column):
        if logic_grid[y, x] == 1:
            color_grid[y, x] = random.choice(initOptions)
        else:
            color_grid[y, x] = BLACK  # or None

def draw_grid():
    for y in range(row):
        for x in range(column):
            color = color_grid[y, x] if logic_grid[y, x] == 1 else BLACK
            pygame.draw.rect(screen, color, (x * sizeOfCell, y * sizeOfCell, sizeOfCell, sizeOfCell))

def update_grid():
    global logic_grid, color_grid
    new_logic = logic_grid.copy()
    new_color = color_grid.copy()

    for y in range(row):
        for x in range(column):
            neighbors = np.sum(logic_grid[max(0, y-1):min(row, y+2),
                                           max(0, x-1):min(column, x+2)]) - logic_grid[y, x]

            if logic_grid[y, x] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_logic[y, x] = 0
                    new_color[y, x] = BLACK  # cell dies, color fades
            elif logic_grid[y, x] == 0 and neighbors == 3:
                new_logic[y, x] = 1

                # find alive neighbor colors and mix them
                neighbor_colors = []
                for ny in range(max(0, y-1), min(row, y+2)):
                    for nx in range(max(0, x-1), min(column, x+2)):
                        if (ny != y or nx != x) and logic_grid[ny, nx] == 1:
                            neighbor_colors.append(color_grid[ny, nx])

                if neighbor_colors:
                    avg_color = tuple(np.mean(neighbor_colors, axis=0).astype(int))
                    new_color[y, x] = avg_color
                else:
                    new_color[y, x] = random.choice(initOptions)

    logic_grid = new_logic
    color_grid = new_color

# 'game' loop
running = True
while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_TAB:
                redo_grid()
            elif event.key == pygame.K_RETURN:
                refresh_grid()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_down = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
    if mouse_down:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // sizeOfCell
        grid_y = mouse_y // sizeOfCell

        if 0 <= grid_x < column and 0 <= grid_y < row:
            logic_grid[grid_y, grid_x] = 1
            color_grid[grid_y, grid_x] = random.choice(initOptions)

    if not paused:
        update_grid()
    draw_grid()
    pygame.display.flip()

pygame.quit()
