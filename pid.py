class PID:
    def __init__(self, p: float, i: float, d: float, min_val: int, max_val:
    int):
        self.p = p
        self.i = i
        self.d = d
        self.value = 0
        self.err = 0
        self.min = min_val
        self.max = max_val

    def update(self, err: int) -> int:
        new_value = int(self.p * err + self.i * (err - self.err))
        if new_value > self.max:
            new_value = self.max
        elif new_value < self.min:
            new_value = self.min
        self.value = new_value
        self.err = err
        # print(f'new value: {self.value}, new err {self.err}')
        return self.value


