from dataclasses import dataclass

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