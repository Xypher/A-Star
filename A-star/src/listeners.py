import pygame as pg
import colors
import threading


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


def animate(grid):
    
    grid.init() # initialize data structures for the algorithm
    animation = grid.iter()
    clock = pg.time.Clock()
    while grid.animation_running:
        if grid.pause: continue

        clock.tick(grid.animation_speed)
        
        try: next(animation)
        except StopIteration: break

    
    grid.animation_running = False
    grid.animation_finished = True


def start_animation(grid):
    global t
    if grid.animation_running or grid.source == (-1, -1) or grid.dest == (-1, -1):
        return
    grid.animation_running = True
    grid.pause = False
    t = threading.Thread(target=animate, args=(grid,))
    t.daemon=True
    t.start()


def reset(grid):

    animation_was_running = grid.animation_running
    grid.animation_running = False
    if 't' in globals() and animation_was_running:
        t.join()      
    grid.reset()

def pause_animation(grid):
    grid.pause = not grid.pause


def clear(grid):
    animation_was_running = grid.animation_running
    grid.animation_running = False
    if 't' in globals() and animation_was_running:
        t.join()    
    grid.clear()



def handle_keyboard(grid, events, keys):
    for event in events:
        if event.type == pg.KEYDOWN:
            if keys[pg.K_SPACE]:
                start_animation(grid)

            if keys[pg.K_r]:
                reset(grid)

            if keys[pg.K_c]:
                clear(grid)

            if keys[pg.K_p] and grid.animation_running:
                pause_animation(grid)


def listen(grid, sidebar, events, keys):
    handle_mouse(grid, events)
    handle_keyboard(grid, events, keys)
    sidebar.listen(events)

    if grid.animation_finished and 't' in globals():
        grid.animation_finished = False
        t.join()
