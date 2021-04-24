import pygame as pg
import constants as cts
from Entities import Block, Grid
from listeners import listen
import colors
import threading

def init():
    cts.init(16)
    pg.init()
    pg.font.init()
    win = pg.display.set_mode((cts.screen_width, cts.screen_height))
    pg.display.set_caption("A* Algorithm")
    win.fill(colors.background)
    clock = pg.time.Clock()
    blocks = []
    for i in range(cts.blocks_count):
            blocks.append([
                    Block(i, j, cts.INF, colors.passable, win) 
                    for j in range(cts.blocks_count)
                ])
    return win, clock, blocks


def draw(grid):
    for row in grid.blocks:
        for block in row:
            block.redraw(grid.win)

    pg.display.update()

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


def main():
    grid: Grid = Grid(*init())

    running = True

    while running:
        grid.clock.tick(60)
        events = pg.event.get()
        keys = pg.key.get_pressed()
        
        for event in events:
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if keys[pg.K_SPACE] and not grid.animation_running:
                    grid.animation_running = True
                    grid.pause = False
                    t = threading.Thread(target=animate, args=(grid,))
                    t.daemon=True
                    t.start()

                if keys[pg.K_r]:
                    animation_was_running = grid.animation_running
                    grid.animation_running = False
                    if 't' in locals() and animation_was_running:
                        t.join()
                    
                    grid.reset()

                if keys[pg.K_a]:
                    grid.animation_speed = max(10, grid.animation_speed - 10)
                if keys[pg.K_d]:
                    
                    grid.animation_speed = min(120, grid.animation_speed + 10)

                if keys[pg.K_p] and grid.animation_running:
                    grid.pause = not grid.pause
                
                if keys[pg.K_c]:
                    animation_was_running = grid.animation_running
                    grid.animation_running = False
                    if 't' in locals() and animation_was_running:
                        t.join()
                    
                    grid.clear()

            if grid.animation_finished:
                grid.animation_finished = False
                t.join()


        listen(events, grid, keys)
        draw(grid)


    pg.quit() # end the programm


if __name__ == "__main__": main()