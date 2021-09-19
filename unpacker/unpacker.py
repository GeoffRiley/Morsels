from collections import UserDict
from typing import Any, Iterator


class Unpacker(UserDict):
    def __init__(self, dictionary: dict = None) -> None:
        self.data = {}
        if isinstance(dictionary, dict):
            for k, v in dictionary.items():
                setattr(self, k, v)

    def __getitem__(self, keys) -> Any:
        if not isinstance(keys, tuple):
            return self.data.get(keys)
        lst = [self.data.get(key) for key in keys]
        return tuple(lst)

    def __setitem__(self, keys: str, values: Any) -> None:
        if not isinstance(keys, tuple):
            self.data[keys] = values
        else:
            values = list(values)
            if len(keys) != len(values):
                raise ValueError
            for k, v in zip(keys, values):
                self.data[k] = v

    def __setattr__(self, key: str, value: Any) -> None:
        if key != 'data':
            self.data[key] = value
        super().__setattr__(key, value)

    def __iter__(self) -> Iterator[Any]:
        yield from self.data.values()

    def __repr__(self) -> str:
        params = ", ".join(f"{k}={v!r}" for k, v in self.data.items())
        return f"{self.__class__.__name__}({params})"
