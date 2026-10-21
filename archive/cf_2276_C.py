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

t = nextInt()
while t > 0:
    N = nextInt()
    K = nextInt()
    A = [0]*N
    pSum = [0]*N
    for i in range(0, N, 1):
        A[i] = nextInt() % K
        if i == 0:
            pSum[0] = A[0]
        else :
            pSum[i] = (pSum[i - 1] + A[i]) % K
    t -= 1

    # print(A)

    # Pass 1. find answer for pref that start at L = 0
    cnt = [0]*K
    # curSum = 0
    for i in range(0, N, 1):
        # curSum += A[i]
        # curSum %= K
        # print(pSum[i], end=' ')
        if i >= K:
            cnt[pSum[i]] += 1
    finalAnswer = cnt[0]
    # print()
    # print("fin a", finalAnswer)

    # Pass 2. find ans for all L = [1..n-1]

    # rollingAdd = 0
    for L in range(1, N, 1):
        # remove L - 1
        if K + L - 1 < N and cnt[pSum[K + L - 1]] > 0 :
            cnt[pSum[K + L - 1]] -= 1
        finalAnswer += cnt[pSum[L - 1]]
        # print("fin a", cnt[pSum[L - 1]])

    print(finalAnswer, end="\n")
    # print()



# print(nextInt() + nextInt())
# print(nextToken()[3])

# print(int(input() + input()))

# print("?", 1, 5, end="\n", flush=False)
# print("? 1 5")
