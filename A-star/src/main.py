import pygame as pg
import constants as cts
from Entities import Grid, SideBar
from listeners import listen
import colors

def init():
    cts.init(16)
    pg.init()
    pg.font.init()
    win = pg.display.set_mode((cts.screen_width, cts.screen_height))
    pg.display.set_caption("A* Algorithm")
    clock = pg.time.Clock()

    return win, clock


def draw(grid, sidebar, win):
    win.fill(colors.background)
    sidebar.draw()
    grid.draw()
    pg.display.update()



def main():
    win, clock = init()
    grid: Grid = Grid(win, clock, 8)
    sidebar: SideBar = SideBar(win, grid)
    
    running = True

    while running:
        clock.tick(60)
        events = pg.event.get()
        keys = pg.key.get_pressed()
        
        for event in events:
            if event.type == pg.QUIT:
                running = False

        listen(grid, sidebar, events, keys)
        draw(grid, sidebar, win)


    pg.quit() # end the programm


if __name__ == "__main__": main()