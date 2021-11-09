from typing import Any

SEMAPHORE = object()


class computed_property:
    def __init__(self, *attr_names):
        self.attr_names = attr_names
        self.fset = self.fget = None
        self._current_value = {}

    def __call__(self, func: callable) -> 'computed_property':
        self.fget = func
        return self

    def __get__(self, obj: object, _) -> 'computed_property':
        if obj is None:
            return self

        current_value = tuple(
            getattr(obj, a, SEMAPHORE) for a in self.attr_names)

        if current_value != self._current_value.get(hash(obj),
                                                    (SEMAPHORE, ))[0]:
            self._current_value[hash(obj)] = (current_value, self.fget(obj))

        return self._current_value[hash(obj)][1]

    def __set__(self, obj: object, value: Any):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, _):
        raise AttributeError("can't delete attribute")

    def setter(self, fset: callable) -> 'computed_property':
        self.fset = fset
        return self
