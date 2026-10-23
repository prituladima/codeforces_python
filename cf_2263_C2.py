from dataclasses import dataclass
from typing import Any

@dataclass
class Pair:
    first: int
    second: int

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
    # max_ = 0
    cSum = [0] * (n + 1)

    list = []

    for i in range(0, n, 1):
        # we always cross out later? can't prove it
        if (i + 1) * a[i] < n :
            cSum[(i + 1) * a[i]] += 1
        if (i + 1) * (a[i] + 1) < n :
            cSum[(i + 1) * (a[i] + 1)] -= 1
            # max_ = max(max_, (i + 1) * (a[i] + 1))
        list.append(Pair((i + 1) * a[i], (i + 1) * (a[i] + 1)))


    ans = 0
    for i in range(0, n, 1) :
        cSum[i] += cSum[i - 1]
        if cSum[i] == 0:
            ans += 1
    # print(ans)
    # for i in range(0, n, 1) :
    #     if cSum[i] == 0:
    #         print(i, end = ' ')

    MOD = 1000000007
    pow = [1]*n
    for _ in range(1, n, 1):
        pow[_] = pow[_ - 1] * 2
        pow[_] %= MOD

    print(pow)
    print(list)

    ans = 1
    for i in range(1, len(list), 1):
        if list[i].first >= list[i - 1].second:
            len_ = list[i].first - list[i - 1].second
            for _ in range (0, len_ // (i + 1), 1):
                ans *= (pow[i + 1] - 1 + MOD) % MOD
                ans %= MOD
            if len_ % (i + 1) != 0:
                ans *= (pow[len_ % (i + 1)] - 1 + MOD) % MOD
                ans %= MOD

    if list[-1].second < n:
        ans *= pow [n - list[-1].second]
        ans %= MOD

    # for _ in range(0, n - max_, 1):
    #     ans *= 2
    #     ans %= MOD


    # print()
    print(ans)

t = nextInt()
while t > 0:
    t -= 1
    solve()