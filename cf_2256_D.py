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

    if n <= 3:
        # n >= 4 for ans to be possible to > 1
        print(1)
        return
    #s[L] == s[R], so answer is not C(n, cnt(1))

    # s[l] and s[r]
    # [l + 1, r - 1] have to be not palindrome

    # N^2 solution
    # ans[j] = ans[j - 1]
    # ans[j] += ans[i] where [i + 1, j - 1] not palindrome

    # ans[j] = cnt1 - cntPalindromes[j - 1]
    # cntP[j - 1] >= cntP[j] linear overal??

    # all suf of pref at j - 1
    # we have cnt0
    # j = pal + nPal
    # nP = all(0) + part(1)




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