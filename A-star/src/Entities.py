import pygame as pg
import constants as cts


class Grid:
    def __init__(self, win, clock, blocks):
        self.win = win
        self.clock = clock
        self.blocks = blocks
        self.last_mouse_button_pressed = -1
        self.source = (-1, -1)
        self.dest = (-1, -1)



class Block:
    def __init__(self, i, j, color, win):
        self.i = i
        self.j = j
        self.x = i * (cts.block_width + cts.offset)
        self.y = j * (cts.block_width + cts.offset)
        self.color = color
        self.rect = pg.draw.rect(win, color, (self.x, self.y, cts.block_width, cts.block_height))
    
    def redraw(self, win):
        self.rect=pg.draw.rect(win, self.color, (self.x, self.y, cts.block_width, cts.block_height))

    
    def is_clicked(self, win):
        return self.rect.collidepoint(pg.mouse.get_pos())

    def index(self):
        return self.i, self.j