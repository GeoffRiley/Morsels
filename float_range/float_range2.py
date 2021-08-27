from math import ceil


class float_range:
    def __init__(self, start: float, stop: float = None, step: float = None):
        if stop is None:
            start, stop, step = 0, start, 1
        elif step is None:
            step = 1
        self.start = start
        self.stop = stop
        self.step = step
        self.current = start

    def __len__(self) -> int:
        if self.step < 0:
            ret = ceil((self.current - self.stop) / -self.step)
        else:
            ret = ceil((self.stop - self.current) / self.step)
        return ret if ret > 0 else 0

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        ret_val = self.current
        if ((self.step > 0 and float(self.current) < float(self.stop))
                or (self.step < 0 and float(self.current) > float(self.stop))):
            self.current += self.step
            return ret_val
        raise StopIteration

    def __getitem__(self, idx: int):
        if isinstance(idx, slice):
            return [self[i] for i in range(*idx.indices(self.__len__()))]
        if idx < 0:
            idx = self.__len__() + idx
        ret_val = self.start + self.step * idx
        if (idx < 0) or (self.step < 0
                         and not (self.stop < ret_val <= self.start)) or (
                             self.step > 0
                             and not (self.start <= ret_val < self.stop)):
            raise IndexError(f"{self.__class__.__name__} index out of range")
        return ret_val
