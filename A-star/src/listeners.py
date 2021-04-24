import pygame as pg
import colors


def get_latest_mouse_button_click(grid):
    mouse_clicks = pg.mouse.get_pressed()
    for i in range(3):
        if mouse_clicks[i]:
            grid.last_mouse_button_pressed = i
            return


def handle_mouse(grid, events):
    clicked_blocks = []

    get_latest_mouse_button_click(grid)
    if any([event.type == pg.MOUSEBUTTONUP for event in events]):
        for row in grid.blocks:
            for block in row:
                if block.is_clicked(grid.win):
                    clicked_blocks.append(block)

    for block in clicked_blocks:
        if grid.last_mouse_button_pressed == 2:
            if block.index() == grid.source:
                grid.source = (-1, -1)
                block.color = colors.passable

            elif grid.source == (-1, -1) and block.color == colors.passable:
                block.color = colors.source
                grid.source = block.index()
            
            elif grid.source != (-1, -1) and block.color == colors.passable:
                grid.blocks[grid.source[0]][grid.source[1]].color = colors.passable
                block.color = colors.source
                grid.source = block.index()

        elif grid.last_mouse_button_pressed == 1:
            if block.index() == grid.dest:
                grid.dest = (-1, -1)
                block.color = colors.passable

            elif grid.dest != (-1, -1) and block.color == colors.passable:
                grid.blocks[grid.dest[0]][grid.dest[1]].color = colors.passable
                block.color = colors.dest
                grid.dest = block.index()

            elif grid.dest == (-1, -1) and block.color == colors.passable:
                block.color = colors.dest
                grid.dest = block.index()

        elif grid.last_mouse_button_pressed == 0:
            if block.color == colors.passable:
                block.color = colors.blocked
            elif block.color == colors.blocked:
                block.color = colors.passable


def handle_keyboard(events, grid, keys):
    pass

def listen(events, grid, keys):
    handle_mouse(grid, events)
