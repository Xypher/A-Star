import pygame as pg
import constants as cts
import heapq as hq
import colors


class Block:
    def __init__(self, r, c, f, color, win):
        self.r = r
        self.c = c
        self.f = f
        self.x = r * (cts.block_width + cts.offset)
        self.y = c * (cts.block_width + cts.offset)
        self.color = color
        self.rect = pg.draw.rect(win, color, (self.x, self.y, cts.block_width, cts.block_height))
    
    def redraw(self, win):
        self.rect=pg.draw.rect(win, self.color, (self.x, self.y, cts.block_width, cts.block_height))
    
    def is_clicked(self, win):
        return self.rect.collidepoint(pg.mouse.get_pos())

    def index(self):
        return self.r, self.c
        

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):   
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
    def __init__(self, win, clock, blocks):
        self.win = win
        self.clock = clock
        self.blocks = blocks
        self.last_mouse_button_pressed = -1
        self.source = (-1, -1)
        self.dest = (-1, -1)
        self.path = self.prev = self.dist = self.searched = None


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


    def reset(self):
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
    

    
    #returns true if done
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