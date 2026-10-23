from dataclasses import dataclass
from heapq import heappush, heappop


@dataclass
class Segment:
    sum: int
    cnt: int
    # L: Segment
    # R: Segment
    def __init__(self):
        self.sum = 0
        self.cnt = 0
        pass

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

class SegTree :

    def __init__(self):
        self.root = Segment()

    def addInternal(self, cur, L, R, value):
        cur.sum += value
        cur.cnt += 1
        if R - L > 1:
            M = (L + R) // 2
            if value < M:
                if not hasattr(cur, 'L'):
                    cur.L = Segment()
                self.addInternal(cur.L, L, M, value)
            else :
                if not hasattr(cur, 'R'):
                    cur.R = Segment()
                self.addInternal(cur.R, M, R, value)

    def add(self, value):
        # if not hasattr(self, 'root'):
        #     self.root = Segment()
        self.addInternal(self.root, 1, 1000000001, value)

    def getSum(self, cur):
        if cur is not None :
            return cur.sum
        return 0

    def getCnt(self, cur):
        if cur is not None:
            return cur.cnt
        return 0

    def minCntToGetTergetInteranl(self, cur, L, R, t):
        if R - L > 1:
            M = (L + R) // 2
            if  self.getSum(cur.R if hasattr(cur, 'R') else None) < t:
                return self.getCnt(cur.R if hasattr(cur, 'R') else None) + self.minCntToGetTergetInteranl(cur.L, L, M, t - self.getSum(cur.R if hasattr(cur, 'R') else None))
            else :
                return self.minCntToGetTergetInteranl(cur.R, M, R, t)
        else:
            val = cur.sum // cur.cnt
            return (t + val - 1) // val


    def minCntToGetTerget(self, targetSum):
        return self.minCntToGetTergetInteranl(self.root, 1, 1000000001, targetSum)




def solve():
    n = nextInt()
    m = nextInt()
    v = [0]*n
    for i in range(0, n, 1):
        v[i] = nextInt()
    a = []
    for i in range(n):
        a.append([])
        for j in range(m):
            a[i].append(nextInt())

    finalAnswer = m
    # st = SegTree()

    h = []
    sumInHeap = 0
    for i in range(n - 1, -1, -1) :
        if finalAnswer == 1:
            break

        for j in range(m):
            # st.add(a[i][j])
            heappush(h, a[i][j])
            sumInHeap += a[i][j]
        while len(h) >= finalAnswer:
            x = heappop(h)
            sumInHeap -= x

        if sumInHeap >= v[i]:
            list = []
            while sumInHeap >= v[i]:
                x = heappop(h)
                sumInHeap -= x
                list.append(x)
            finalAnswer = min(finalAnswer, len(h) + 1)
            for _ in list:
                heappush(h, _)
                sumInHeap += _

        # if st.root.sum >= v[i]:
        #     finalAnswer = min(finalAnswer, st.minCntToGetTerget(v[i]))




    print(finalAnswer)



t = nextInt()
while t > 0:
    t -= 1
    solve()