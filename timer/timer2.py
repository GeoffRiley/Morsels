from collections import defaultdict
from contextlib import contextmanager
from time import perf_counter

SEMAPHORE = object()


class Timer:
    _instances = {}

    def __new__(cls, name: str = SEMAPHORE) -> 'Timer':
        if name is SEMAPHORE:
            return super().__new__(cls)
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]

    def __init__(self, name: str = None) -> None:
        self.start_time = None
        self.runs = []
        self.splits = defaultdict(Timer)
        self.anonymous_index = 0
        self._name = name

    def __enter__(self):
        self.stop = None
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = perf_counter()
        self.runs.append(self.elapsed)
        return False

    @property
    def elapsed(self):
        if self.start is None:
            raise ValueError('Unused timer')
        if self.stop is None:
            return perf_counter() - self.start
        return self.stop - self.start

    @contextmanager
    def split(self, name: str = None):
        if self.stop is not None:
            raise RuntimeError(
                'Cannot split because parent timer is not running')
        if name is None:
            name = self.anonymous_index
            self.anonymous_index += 1
        with self.splits[name] as t:
            yield t

    def __getitem__(self, index: int) -> 'Timer':
        return self.splits.get(index, None)
