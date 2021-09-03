from collections.abc import Mapping as AMapping
from typing import Any, Mapping, Sequence


class ProxyDict(AMapping):
    def __init__(self, mapping: Mapping) -> None:
        self._mapping = mapping
        super().__init__()

    def __getitem__(self, i: Any) -> Any:
        return self._mapping[i]

    def __len__(self) -> int:
        return len(self._mapping)

    def __iter__(self) -> Sequence[Any]:
        return self._mapping.__iter__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._mapping!r})"
