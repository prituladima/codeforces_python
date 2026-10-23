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

    cSum = [0] * (n + 1)
    for i in range(0, n, 1):
        if (i + 1) * a[i] < n :
            cSum[(i + 1) * a[i]] += 1
        if (i + 1) * (a[i] + 1) < n :
            cSum[(i + 1) * (a[i] + 1)] -= 1
    ans = 0
    for i in range(0, n, 1) :
        cSum[i] += cSum[i - 1]
        if cSum[i] == 0:
            ans += 1
    print(ans)
    for i in range(0, n, 1) :
        if cSum[i] == 0:
            print(i, end = ' ')

    print()

t = nextInt()
while t > 0:
    t -= 1
    solve()