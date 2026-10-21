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


t = nextInt()
while t > 0:
    t -= 1
    solve()