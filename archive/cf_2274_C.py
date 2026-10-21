from typing import Callable

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

def lowerBound(L, R, predicate):
    while R - L > 1:
        M = L + (R - L) // 2
        if predicate(M) :
            R = M
        else :
            L = M
    return R

def unpack(x):
    needEl = 0
    for i in range (1, x + 1 , 1):
        needEl += (x // i) * i

    return needEl

def check(x, n):
    # we unpack pos ans to n
    needEl = 0
    for i in range (1, x + 1, 1):
        needEl += (x // i) * i

    return needEl >= n


def solve():
    n = nextInt()

    # We look for min from maxAnswers. Use binary search by the answer.
    j = lowerBound(0, n, lambda x: check(x, n) )
    print(j)
    cur = n
    list = []
    for i in range (j, 0, -1):
        # how much group we print ?
        for g in range (1, j // i + 1,  1):
            if n - len(list) >= i:
                for k in range (0, i, 1):
                    list.append(cur)
                cur -= 1
    for _ in list:
        print(_, end=' ')
    print()


# for x in range (1, 6, 1):
#     print(unpack(x))
#
t = nextInt()
while t > 0:
    t -= 1
    solve()

