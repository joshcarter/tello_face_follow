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
