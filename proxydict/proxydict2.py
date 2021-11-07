from collections import ChainMap
from collections.abc import Mapping as AMapping
from reprlib import recursive_repr
from typing import Any, List, Mapping, Sequence


class ProxyDict(AMapping):
    def __init__(self, *mappings: List[Mapping]) -> None:
        self.maps = list(mappings)
        super().__init__()

    def __getitem__(self, i: Any) -> Any:
        return self._mapping[i]

    def __len__(self) -> int:
        return len(self._mapping)

    def __iter__(self) -> Sequence[Any]:
        return self._mapping.__iter__()

    @property
    def _mapping(self) -> Sequence[Any]:
        return dict(ChainMap(*self.maps[::-1]))

    @recursive_repr('ProxyDict(...)')
    def __repr__(self) -> str:
        parameters = ', '.join(repr(m) for m in self.maps)
        return f"{self.__class__.__name__}({parameters})"
