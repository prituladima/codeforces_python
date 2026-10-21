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
    MOD = 998244353
    n = nextInt()
    a = [0]*n
    for i in range(0, n, 1):
        a[i] = nextInt()
    if n == 1:
        print(0)
    elif n == 2:
        print(abs(a[0] - a[1]) % MOD)
    else:
        a.sort(reverse=True)
        finalAns = a[0] - a[1]
        combinations = 1
        prefSum = a[0] + a[1]
        for i in range(2, n, 1) :
            contribute = prefSum - i * a[i]

            finalAns *= i
            finalAns += combinations * contribute
            finalAns %= MOD
            prefSum += a[i]
            combinations *= i
            combinations %= MOD
        print(finalAns)


t = nextInt()
while t > 0:
    t -= 1
    solve()
