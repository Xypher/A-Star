import pygame as pg

"""pg.init()
screen_width = 1024
screen_height = 768
win = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("window")
clock = pg.time.Clock()
walk_left = [pg.image.load(f"sprite/L{i}.png") for i in range(1, 10)]
walk_right = [pg.image.load(f"sprite/R{i}.png") for i in range(1, 10)]
stand = pg.image.load("sprite/standing.png")
run = True



class player:
    def __init__(self, x, y , width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.jump = False
        self.jump_count = 10
        self.left = False
        self.right = False 
        self.walk_count = 0

    def draw(self):
        self.walk_count %= 27

        if self.left:
            win.blit(walk_left[self.walk_count//3], (self.x, self.y))
        elif self.right:
            win.blit(walk_right[self.walk_count//3], (self.x, self.y))
        else:
            win.blit(stand, (self.x, self.y))
            self.walk_count = 0
        self.walk_count += int(self.left or self.right)
    


plr = player(300, 410, 64, 64)

def draw():
    global plr
    win.fill((0, 0, 0))
    plr.draw()
    pg.display.update()



 

while run:
    clock.tick(27)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT] :
        plr.x = max(plr.x-plr.vel, 0)
        plr.left = True
        plr.right = False
    elif keys[pg.K_RIGHT]:
        plr.x = min(plr.x + plr.vel, screen_width - plr.width)
        plr.left = False
        plr.right = True

    else:
        plr.left = plr.right = False

    if not plr.jump:
        if keys[pg.K_SPACE]:
            plr.jump = True


    else:
        if plr.jump_count >= -10:
            if plr.jump_count > 0:
                plr.y = max(0, plr.y - plr.jump_count ** 2 / 2)
            else:
                plr.y = min(screen_height - plr.height, plr.y + plr.jump_count ** 2 / 2)
            plr.jump_count -= 1
        else:
            plr.jump = False
            plr.jump_count= 10

        

    
    #rect = pg.draw.rect(win, (0, 0, 255), (x, y, width, height))

    #pg.display.update()
    draw()

pg.quit()"""

import threading as thd
import time

def summation(n: int):
    global sum
    sum = 0
    for i in range(1, n+1):
        sum += i

    

def product(n: int):
    global prod
    prod = 1
    for i in range(1, n+1):
        prod *= i


def sync():
    summation(int(1e5))
    product(int(1e5))
    print(sum, len(str(prod)))

def parallel():
    t1 = thd.Thread(target=summation, args=(int(1e5),))
    t2 = thd.Thread(target=product, args=(int(1e5),))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

    print(sum, len(str(prod)))

start_time = time.time()
parallel()
print("execution time is:  %s seconds" % (time.time() - start_time))



