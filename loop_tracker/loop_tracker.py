from typing import Iterable

SEMAPHORE = object()


class loop_tracker:
    def __init__(self, iterator: Iterable) -> None:
        self._it = iter(iterator)
        self._count = 0
        self._empty_count = 0
        self._held_item = SEMAPHORE
        self._first_value = SEMAPHORE
        self._last_value = SEMAPHORE

    def __iter__(self):
        return self

    def __next__(self):
        value = self._next_iter_()

        if value is SEMAPHORE:
            self._empty_count += 1
            raise StopIteration

        self._last_value = value
        self._count += 1
        return value

    def __len__(self):
        return self._count

    def _next_iter_(self, remove_from_queue=True):
        if self._held_item is SEMAPHORE:
            value = next(self._it, SEMAPHORE)
        else:
            value = self._held_item

        self._held_item = SEMAPHORE if remove_from_queue else value

        if self._first_value is SEMAPHORE:
            self._first_value = value
        return value

    def is_empty(self):
        value = self._next_iter_(False)
        return value is SEMAPHORE

    @property
    def empty_accesses(self):
        return self._empty_count

    @property
    def first(self):
        self._next_iter_(False)
        if self._first_value is SEMAPHORE:
            raise AttributeError(
                "iterable has no first attribute (it's empty)")
        return self._first_value

    @property
    def last(self):
        if self._last_value is SEMAPHORE:
            raise AttributeError('no last item yet (no looping performed yet)')
        return self._last_value
