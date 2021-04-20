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
                    Block(i, j, cts.INF, colors.passable, win) 
                    for j in range(cts.blocks_count)
                ])
    return win, clock, blocks


def draw(events):
    for row in grid.blocks:
        for block in row:
            block.redraw(grid.win)

    pg.display.update()


grid: Grid = Grid(*init())

running = True
animation_running = False
animation = None

while running:
    grid.clock.tick(30)
    events = pg.event.get()
    keys = pg.key.get_pressed()

    for event in events:
        if event.type == pg.QUIT:
            running = False

        if keys[pg.K_SPACE] and not animation_running:
            animation_running = True
            grid.init()
            animation = grid.iter()

        if keys[pg.K_r]:
            animation_running = False
            grid.reset()

    if animation_running == True:
        try: next(animation)
        except StopIteration:
            animation_running = False
            animation = None

    listen(events, grid, keys)

    draw(grid.blocks)


pg.quit() # end the programm
