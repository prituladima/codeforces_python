import sys, threading

MOD = 1000000007
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
#
# def prepareCnk(n):
#     f =[1]*(n + 1)
#     iF = [1]*(n + 1)
#     for i in range(2, n + 1, 1):
#         f[i] = f[i - 1] * i % MOD
#     iF[n] = pow(f[n], MOD - 2, MOD)
#     for i in range(n - 1, 1, -1):
#         iF[i] = iF[i + 1] * (i + 1) % MOD
#
#     return f, iF

def preparePow2 (n):
    pow2 = [1]*(n + 1)
    for _ in range(1, n + 1, 1) :
        pow2[_] *= pow2[_ - 1] * 2 % MOD
    return pow2

pow2 = preparePow2(200000 + 10)

# def getCnk(f, inv_f, n, k):
#     return (f[n] * inv_f[n - k]) % MOD * inv_f[k] % MOD

def solve():
    n = nextInt()
    a = [0]*n
    for i in range(0, n, 1):
        a[i] = nextInt()

    cnt = {}
    for _ in a:
        cnt[_] = cnt.get(_, 0) + 1

    partialAns = {}
    allAns = 1
    for key in cnt:
        allAns *= pow2[cnt[key] - 1]
        allAns %= MOD
        for right in range(cnt[key] - 1, -1, -1) :
            left = cnt[key] - 1 - right
            comb = 1
            if left >= 2:
                comb *= pow2[left - 1]
            if right >= 2:
                comb *= pow2[right - 1]
            partialAns[key] = partialAns.get(key, 0) + comb
            partialAns[key] %= MOD

    # print(partialAns)

    finalAnswer = allAns
    if a[0] == -1:
        for i in range(1, n, 1):
            if a[i] - a[i - 1] == 1 and a[i - 1] != -1 :
                # -1, A, B where -1 - A + B = 0
                localAns = 1
                # localAns = cnt[-1]
                # localAns *= cnt[a[i - 1]]
                # localAns %= MOD
                # localAns *= cnt[a[i]]
                # localAns %= MOD

                # Include
                localAns *= allAns
                localAns %= MOD

                # Exclude
                # localAns *= pow(pow2[cnt[-1] - 1], MOD - 2, MOD)
                # localAns %= MOD
                # localAns *= pow(pow2[cnt[a[i - 1]] - 1], MOD - 2, MOD)
                # localAns %= MOD
                # localAns *= pow(pow2[cnt[a[i]] - 1], MOD - 2, MOD)
                # localAns %= MOD

                # Include back
                # if cnt[-1] - 2 >= 1:
                #     localAns *= pow2[cnt[-1] - 2]
                #     localAns %= MOD
                # if cnt[a[i - 1]] - 2 >= 0:
                #     localAns *= pow2[cnt[a[i - 1]] - 2]
                #     localAns %= MOD
                # if cnt[a[i]] - 2 >= 0:
                #     localAns *= pow2[cnt[a[i]] - 2]
                #     localAns %= MOD

                # localAns *= partialAns[-1]
                # localAns %= MOD
                # localAns *= partialAns[a[i - 1]]
                # localAns %= MOD
                # localAns *= partialAns[a[i]]
                # localAns %= MOD

                finalAnswer += localAns
                finalAnswer %= MOD

    print(finalAnswer)




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