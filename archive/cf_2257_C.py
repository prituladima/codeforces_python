
import sys, threading


def tokens():
    while True:
        for token in input().split():
            yield token

it = tokens()

def nextInt():
    return int(next(it))

def nextToken():
    return next(it)

def nextFloat():
    return float(next(it))

def dfs(from_, hasDam, graph) :

    if hasDam[from_]:
        return from_


    # if hasDam[from_]:
    #     return from_

    for v in graph[from_]:
        f = dfs(v, hasDam, graph)
        if f != 0:
            return f
    return 0

def solve():
    n = nextInt()
    graph = []
    for _ in range(n + 1):
        graph.append([])
    for v in range(2, n + 1, 1):
        p = nextInt()
        graph[p].append(v)

    m = nextInt()
    hasDam = [False] * (n + 1)

    dumbs = []
    for _ in range(m):
        k = nextInt()
        hasDam[k] = True
        dumbs.append(k)


    # if hasDam[1]:
    #     print(len(dumbs) - 1, end=' ')
    #     for d in dumbs:
    #         if d != 1:
    #             print(d, end=' ')
    if len(dumbs) == 1:
        print(0, end=' ')
    else:
            skip = dfs(1, hasDam, graph)
            print(len(dumbs) - 1, end=' ')
            for d in dumbs:
                if d != skip:
                    print(d, end=' ')

    print()

def main():
    t = nextInt()
    while t > 0:
        t -= 1
        solve()

sys.setrecursionlimit(1 << 25)
threading.stack_size(1 << 27)
thread = threading.Thread(target=main)
thread.start()
thread.join()
