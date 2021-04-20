import pygame as pg
import constants as cts
from Entities import Block, Grid
from listeners import listen
import colors
import threading

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


def draw(grid):
    for row in grid.blocks:
        for block in row:
            block.redraw(grid.win)

    pg.display.update()

def animate(grid):
    global animation_running, animation_finished
    
    grid.init() # initialize data structures for the algorithm
    animation = grid.iter()
    clock = pg.time.Clock()
    while animation_running:
        if pause: continue

        clock.tick(animation_speed)
        
        try: next(animation)
        except StopIteration: break

    animation_running = False
    animation_finished = True



def main():
    global animation_running, animation_finished, animation_speed, pause
    grid: Grid = Grid(*init())

    running = True
    animation_running = False
    animation_finished = False
    pause = False
    animation_speed = 60

    while running:
        grid.clock.tick(60)
        events = pg.event.get()
        keys = pg.key.get_pressed()
        
        for event in events:
            if event.type == pg.QUIT:
                running = False

            if keys[pg.K_SPACE] and not animation_running:
                animation_running = True
                pause = False
                t = threading.Thread(target=animate, args=(grid,))
                t.daemon=True
                t.start()

            if keys[pg.K_r]:
                animation_was_running = animation_running
                animation_running = False
                if 't' in locals() and animation_was_running:
                    t.join()
                
                grid.reset()

            if keys[pg.K_a]:
                animation_speed = max(10, animation_speed - 10)
            
            if keys[pg.K_d]:
                animation_speed = min(120, animation_speed + 10)

            if keys[pg.K_p] and animation_running:
                pause = not pause


            if animation_finished:
                animation_finished = False
                t.join()


        listen(events, grid, keys)
        draw(grid)


    pg.quit() # end the programm


if __name__ == "__main__": main()