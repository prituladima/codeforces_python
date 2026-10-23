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
    a = [0]*(2 * n)
    for i in range(0, 2 * n, 1):
        a[i] = nextInt()

    ans = [0] * (2 * n)
    ans[0] = 1
    lookup = [-1] * (n + 1)
    lookup[a[0]] = 0
    for i in range(1, 2 * n, 1):
        ans[i] = ans[i - 1] + 1
        j = lookup[a[i]]
        if j != -1:
            if j == 0:
                ans[i] = max(ans[i], (i + 1) * (i + 1))
            else:
                ans[i] = max(ans[i], ans[j - 1] + (i + 1 - j) * (i + 1 - j))
            lookup[a[i]] = -1
        else :
            lookup[a[i]] = i

    print(ans[2 * n  - 1])

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