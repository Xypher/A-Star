import heapq as hq
from constants import INF
from Entities import Node, Block


def init_grid(grid: list[list[Block]]):


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
        prev.append([Node(-1, -1, -1)] * len(grid[0]))
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
                nei =  Node(curr.r + i, curr.c + j, -1) # neighboring Node

                d = dist[curr.r][curr.c] + 1
                if  d < dist[nei.r][nei.c]:
                    prev[nei.r][nei.c] = curr
                    dist[nei.r][nei.c] = d
                    f[nei.r][nei.c] = d + h(nei , end) 
                    if nei not in searched:
                        hq.heappush(queue, Node(nei.r, nei.c, f[nei.r][nei.c]))

        
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
src= Node(0, 0, INF)
end = Node(4, 4, INF)
h = lambda x, y: max( abs(x.r - y.r), abs(x.c- y.c) )
print(a_star(grid, src, end, h))
