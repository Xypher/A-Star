import heapq as hq
from constants import INF

class node:
    def __init__(self, r: int, c: int, f: int):
        self.r = r; self.c = c; self.f = f
    
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

def valid(grid, cr, cc):
    return (cr >= 0 and
        cr < len(grid) and
        cc >= 0 and
        cc < len(grid[0]) and
        grid[cr][cc] == 1)


def form_path(prev, src, end):
    path = []   
    curr = end
    while(curr != prev[curr.r][curr.c]):
        path.append( curr )
        curr = prev[curr.r][curr.c]
    
    path.append(curr)
    return list(reversed(path))


def a_star(grid: list[list[bool]] , src: (int, int), end: (int, int), h):
    src.f = 0
    queue = [ src ]
    hq.heapify(queue)

    searched = set()

    prev = []; dist = []; f = []
    for i in range(len(grid)):
        prev.append([node(-1, -1, -1)] * len(grid[0]))
        dist.append([INF] * len(grid[0]))
        f.append([INF] * len(grid[0]))

    dist[src.r][src.c] = 0
    prev[src.r][src.c] = src
    f[src.r][src.c] = h(src, end)

    while len(queue) > 0:
        curr = hq.heappop(queue)
        searched.add(curr)
        moves = [0, 1, -1] 
        for i in moves:
            for j in moves:
                if (i, j) == (0, 0) or not valid(grid, curr.r + i, curr.c + j):
                    continue
                nei =  node(curr.r + i, curr.c + j, -1) # neighboring node
                #print(f"current: {curr.r, curr.c} , child: {nei.r, nei.c}")
                d = dist[curr.r][curr.c] + 1
                if  d < dist[nei.r][nei.c]:
                    prev[nei.r][nei.c] = curr
                    dist[nei.r][nei.c] = d
                    f[nei.r][nei.c] = d + h(nei , end) 
                    if nei not in searched:
                        hq.heappush(queue, node(nei.r, nei.c, f[nei.r][nei.c]))

        
    if dist[end.r][end.c] == INF:
        return None
    return form_path(prev, src, end)

grid = [
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1],
]
src= node(0, 0, INF)
end = node(4, 4, INF)
h = lambda x, y: max( abs(x.r - y.r), abs(x.c- y.c) )
print(a_star(grid, src, end, h))



