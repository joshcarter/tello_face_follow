class Range:
    def __init__(self, min_val: int, max_val: int):
        if min_val >= max_val:
            raise f'min_val {min_val} must be less than max_val {max_val}'

        self.min = min_val
        self.max = max_val

    def min(self):
        return self.min

    def max(self):
        return self.max

    def within(self, val: int) -> bool:
        return self.min <= val <= self.max

    def assert_within(self, val: int) -> None:
        if val < self.min:
            raise f'value {val} must be greater than than min_val {self.min}'
        elif val > self.max:
            raise f'value {val} must be less than than than max_val {self.max}'


class Tracker:
    def __init__(self, in_range: Range, target_range: Range, out_range: Range, invert: bool = False):
        # target zone must be fully within in_range
        in_range.assert_within(target_range.min)
        in_range.assert_within(target_range.max)
        self.in_range = in_range
        self.target_range = target_range
        self.out_range = out_range
        self.invert = invert

    def __repr__(self):
        return f'tracker in [{self.in_range.min}, {self.in_range.max}] ' \
               f'target [{self.target_range.min}, {self.target_range.max}] ' \
               f'out [{self.out_range.min}, {self.out_range.max}]'

    def update(self, val: int) -> int:
        if self.target_range.within(val):
            return 0

        # clamp input range
        if val > self.in_range.max:
            val = self.in_range.max
        elif val < self.in_range.min:
            val = self.in_range.min

        in_span = self.in_range.max - self.in_range.min
        out_span = self.out_range.max - self.out_range.min
        scaled_val = float(val - self.in_range.min) / float(in_span)
        out = self.out_range.min + int(scaled_val * out_span)
        if self.invert:
            out *= -1
        return out


def test_tracker():
    t = Tracker(Range(-10, 10), Range(-1,1), Range(-100, 100))
    print(t)

    for val in [0, -1, 1, -2, 2, -5, 5, -10, 10]:
        print(f'val: {val} tracker output: {t.update(val)}')
