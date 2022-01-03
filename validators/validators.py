from abc import ABCMeta, abstractmethod
from weakref import WeakKeyDictionary

SEMAPHORE = object()


class Validator(metaclass=ABCMeta):
    def __set_name__(self, owner, name):
        self._owner = owner.__qualname__.split('.')[-1]
        self._name = name

    def __init__(self, default=SEMAPHORE) -> None:
        self.default = default
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if self.default is SEMAPHORE and instance not in self.data.keys():
            raise AttributeError(
                f"'{self._owner}' object has no attribute '{instance}'")
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        self.validate(value)
        self.data[instance] = value

    @abstractmethod
    def validate(self, value):
        return NotImplemented


class PositiveNumber(Validator):
    def validate(self, value):
        if value <= 0:
            raise ValueError(f"Negative or zero value not allowed: {value}")
        # return value
