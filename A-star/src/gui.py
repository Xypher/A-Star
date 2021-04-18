import pygame as pg
import constants as cts
from sprite import Block
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

def listen(events):
    global blocks, win
    clicked_blocks = []

    if any([event.type == pg.MOUSEBUTTONUP for event in events]):
        for row in blocks:
            for block in row:
                if block.is_clicked(win):
                    clicked_blocks.append(block)

    for block in clicked_blocks:
        block.color = (
            colors.blocked 
            if block.color==colors.passable 
            else colors.passable
        )

def draw(events):
    global win, blocks
    for row in blocks:
        for block in row:
            block.redraw(win)

    pg.display.update()




win, clock, blocks = init()
running = True

while running:
    clock.tick(60)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    listen(events)
    draw(blocks)


pg.quit() # end the programm




