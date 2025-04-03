import numpy as np
from collections import deque

class SlidingWindowAverager:
    def __init__(self, window):
        self.q = deque()
        self.max = window

    def append(self, n):
        self.q.append(n)
        if len(self.q) > self.max:
            self.q.popleft()

    def value(self):
        sum = 0
        for n in self.q:
            sum += n
        return sum // len(self.q)

    def avg(self, n):
        self.append(n)
        return self.value()


        # from https://stackoverflow.com/a/14314054
        # n = len(self.q)
        # ret = np.cumsum(self.q, dtype=float)
        # ret[n:] = ret[n:] - ret[:-n]
        # return (ret[n - 1:] / n)[0]


# def test():
#     a = SlidingWindowAverager(5)
#     a.append(1)
#     print(a.value())
#     a.append(2)
#     print(a.value())
#     a.append(3)
#     print(a.value())
#     a.append(4)
#     print(a.value())
#     a.append(5)
#     print(a.value())
#     a.append(5)
#     print(a.value())
#     a.append(5)
#     print(a.value())
#     a.append(12)
#     print(a.value())
#     a.append(5)
#     print(a.value())
#     a.append(5)
#     print(a.value())
#     a.append(5)
#     print(a.value())
#
