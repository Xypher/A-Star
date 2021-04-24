import pygame as pg
import pygame_widgets as pgw
import constants as cts
import heapq as hq
import colors
from listeners import reset, clear


class Block:
    def __init__(self, r, c, f, color, win):
        self.r = r
        self.c = c
        self.f = f
        self.x = r * (cts.block_width + cts.offset)
        self.y = c * (cts.block_width + cts.offset)
        self.color = color
        self.rect = pg.draw.rect(win, color, (self.x, self.y, cts.block_width, cts.block_height))

    def draw(self, win):
        self.rect=pg.draw.rect(win, self.color, (self.x, self.y, cts.block_width, cts.block_height))
    
    def is_clicked(self, win):
        return self.rect.collidepoint(pg.mouse.get_pos())

    def index(self):
        return self.r, self.c
        

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):   
        if not isinstance(other, Block):
            return False
        return (self.r, self.c) == (other.r, other.c)

    def __ne__(self, other):
            return self.r != other.r or self.c != other.c

    def __hash__(self):
        return hash(self.r) ^ hash(self.c)

    def __str__(self):
        return str((self.r, self.c))

    def __repr__(self):
        return str((self.r, self.c))



class Grid:
    def __init__(self, win, clock, count):
        self.count=count
        self.win = win
        self.clock = clock
        self.last_mouse_button_pressed = -1
        self.source = (-1, -1)
        self.dest = (-1, -1)
        self.path = self.prev = self.dist = self.searched = None

        self.animation_running = False
        self.animation_finished = False
        self.pause = False
        self.animation_speed = 45

        self.build()

    def build(self):
        self.blocks = []
        for i in range(self.count):
            self.blocks.append([
                    Block(i, j, cts.INF, colors.passable, self.win) 
                    for j in range(self.count)
                ])


    def draw(self):
        for row in self.blocks:
            for block in row:
                block.draw(self.win)

    def heuristic(self, block1, block2):
        return max( abs(block1.r - block2.r), abs(block1.c- block2.c) )

    def valid(self, r, c):
        return (r >= 0 and
            r < len(self.blocks) and
            c >= 0 and
            c < len(self.blocks[0]) and
            self.blocks[r][c].color != colors.blocked)


    def form_path(self):    
        if self.dist[self.dest.r][self.dest.c] == cts.INF:
            self.path=None
            return
        
        self.path = []
        current = self.dest
        while(current != self.prev[current.r][current.c]):
            self.path.append( current )
            current = self.prev[current.r][current.c]

        self.path.append(current)


    def reset(self):
        for row in self.blocks:
            for block in row:
                block.color = colors.passable if block.color != colors.blocked else block.color
        self.source = self.dest = (-1, -1)

    def clear(self):
        for row in self.blocks:
            for block in row:
                block.color = colors.passable
        self.source = self.dest = (-1, -1)


    def init(self):
        self.source = self.blocks[self.source[0]][self.source[1]]
        self.dest = self.blocks[self.dest[0]][self.dest[1]]
        
        self.queue = [ self.source ]
        hq.heapify(self.queue)

        self.searched = set()

        self.prev = []; self.dist = []; self.f = []
        for i in range(len(self.blocks)):
            self.prev.append([None] * len(self.blocks[0]))
            self.dist.append([cts.INF] * len(self.blocks[0]))
            for block in self.blocks[i]:
                block.f = cts.INF

        self.dist[self.source.r][self.source.c] = 0
        self.prev[self.source.r][self.source.c] = self.source
        self.source.f = self.heuristic(self.source, self.dest)
    

    def iter(self):
        while len(self.queue) > 0:
            curr = hq.heappop(self.queue)
            curr.color = colors.current
            
            if curr == self.dest:
                return

            self.searched.add(curr)
            moves = [0, 1, -1] 
            for i in moves:
                for j in moves:
                    if (i, j) == (0, 0) or not self.valid(curr.r + i, curr.c + j):
                        continue
                    nei =  self.blocks[curr.r + i][curr.c + j]# neighboring Node

                    d = self.dist[curr.r][curr.c] + 1
                    if  d < self.dist[nei.r][nei.c]:
                        self.prev[nei.r][nei.c] = curr
                        self.dist[nei.r][nei.c] = d
                        nei.f = d + self.heuristic(nei , self.dest) 
                        if nei not in self.searched:
                            hq.heappush(self.queue, nei)

                    nei.color = colors.searched
                    yield nei
            
            curr.color = colors.searched

            self.form_path()

            if self.path != None:
                for block in self.path:
                    block.color = colors.path


class SideBar:

    def __init__(self, win, grid):
        self.win = win
        self.grid_ref = grid
        self.reset_button = pgw.Button(win, 1000, 500, 150, 50,
            text="Reset",
            fontSize=12, margin=10,
            font=pg.font.SysFont("calibri", 12),
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=5, onClick=lambda: reset(grid)
        )

        self.clear_button = pgw.Button(win, 1000, 300, 150, 50,
            text="Clear",
            fontSize=12, margin=10,
            font=pg.font.SysFont("calibri", 12),
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=5, onClick=lambda: clear(grid)
        )

        self.animation_speed_slider = pgw.Slider(win, 1000, 800, 200, 20, 
            min=10, max=120, step=1, initial=45, curved=True,
        )

        self.block_count_slider = pgw.Slider(win, 1000, 900, 300, 20, 
            min=4, max=16, step=2, initial=8, curved=True,
        )



    def draw(self):
        self.reset_button.draw()
        self.clear_button.draw()
        self.animation_speed_slider.draw()
        self.block_count_slider.draw()

    def listen(self, events):
        self.reset_button.listen(events)
        self.clear_button.listen(events)
        self.animation_speed_slider.listen(events)
        self.block_count_slider.listen(events)

        self.grid_ref.animation_speed = int(self.animation_speed_slider.getValue())

        if int(self.block_count_slider.getValue()) != self.grid_ref.count:
            clear(self.grid_ref)
            self.grid_ref.count=int(self.block_count_slider.getValue())
            
