# from contextlib import ContextDecorator
from statistics import mean, median
from time import time
from typing import Any, Callable


class Timer:  # (ContextDecorator):
    def __init__(self, func=None) -> None:
        super().__init__()
        self.start = self.stop = None
        self.runs = []
        self._func = func

    def __enter__(self):
        self.stop = None
        self.start = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = time()
        self.runs.append(self.elapsed)
        return False

    def __call__(self, *args, **kwargs) -> Callable:
        with self:
            result = self._func(*args, **kwargs)
        return result

    @property
    def elapsed(self):
        if self.start is None:
            raise ValueError('Unused timer')
        if self.stop is None:
            return time() - self.start
        return self.stop - self.start

    _stat_funcs = {
        'mean': mean,
        'median': median,
        'min': min,
        'max': max,
    }

    def __getattribute__(self, name: str) -> Any:
        if name in Timer._stat_funcs:
            return Timer._stat_funcs[name](self.runs)
        return super().__getattribute__(name)
