import sys, threading

def tokens():
    while True:
        for token in input().split():
            yield token

it = tokens()

def nextInt():
    return int(next(it))

def nextIntArray(n):
    a = [0] * n
    for i in range(n):
        a[i] = nextInt()
    return a

def nextToken():
    return next(it)

def nextFloat():
    return float(next(it))

def solve():
    n = nextInt()
    k = nextInt()
    s = nextToken()

    # for k = 1
    # s[i] == 1 and s[(i + 1) % (2 * n)] == 0

    # why team can skip passing?
    # the goal is not only win but also maximize points.
    R = 0
    B = 0
    for i in range(2 * n):
        if s[i] == '1':
            # even and unmovable
            if i % 2 == 0 and s[i] == '1' and s[(i + 1) % (2 * n)] == '1':
                B += 1
            if i % 2 == 1 and s[i] == '1' and s[(i + 1) % (2 * n)] == '1':
                R += 1
            if i % 2 == 0 and s[i] == '1' and s[(i + 1) % (2 * n)] == '0':
                R += 1
            if i % 2 == 1 and s[i] == '1' and s[(i + 1) % (2 * n)] == '0':
                B += 1


    print (R, B)


def main():
    t = nextInt()
    for _ in range(t):
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