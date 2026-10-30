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
    MOD = 998244353
    n = nextInt()
    s = nextToken()

    pat = "0011" * n
    ans = 0
    for offset in range(4):
        cnt = 0
        for i in range(n):
            if s[i] == '?' or s[i] == pat[i + offset]:
               cnt += 1
        if cnt == n:
            ans += 1

    print(ans)
    # answer have to be periodic 110011
    #

    # when impossible
    # 1?1 and 0?0
    #
    # print 0

    # when 1 way
    # 0?1 and 1?0
    # insert *=2 op
    # this doesn't impact the rest

    # edges
    # ?__, __? * = 1 or 2

    # 10??????10 this doesn't impact as well and is always 1




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