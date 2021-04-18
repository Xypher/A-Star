import pygame as pg
import constants as cts
from Entities import Block, Grid
from listeners import listen
import colors

def init():
    pg.init()
    win = pg.display.set_mode((cts.screen_width, cts.screen_height))
    pg.display.set_caption("A* Algorithm")
    clock = pg.time.Clock()
    blocks = []
    for i in range(cts.blocks_count):
            blocks.append([
                    Block(i, j, colors.passable, win) 
                    for j in range(cts.blocks_count)
                ])
    return win, clock, blocks

def get_grid():
    return grid


def draw(events):
    for row in grid.blocks:
        for block in row:
            block.redraw(grid.win)

    pg.display.update()


grid = Grid(*init())

running = True

while running:
    grid.clock.tick(60)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    listen(events, grid)
    draw(grid.blocks)


pg.quit() # end the programm
