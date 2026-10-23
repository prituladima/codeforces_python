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

def solve():
    n = nextInt()
    a = [0]*n
    for i in range(0, n, 1):
        a[i] = nextInt()


def main():
    t = nextInt()
    while t > 0:
        t -= 1
        solve()

INCREASED_RECURSION_LIMIT = False

if INCREASED_RECURSION_LIMIT:
    sys.setrecursionlimit(1 << 25)
    threading.stack_size(1 << 27)
    thread = threading.Thread(target=main)
    thread.start()
    thread.join()
else:
    main()