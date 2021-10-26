from collections.abc import Sequence
from typing import Any, Iterable, Union


class SliceView:
    def __init__(self, it, *, start=None, stop=None, step=None) -> None:
        start, stop, step = slice(start, stop, step).indices(len(it))
        self._data = it
        self._range = range(start, stop, step)

    def __len__(self):
        return len(self._range)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SliceView(self,
                             start=index.start,
                             stop=index.stop,
                             step=index.step)
        return self._data[self._range[index]]


class ChainSequence(Sequence):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.sequences = list(args)

    def __len__(self) -> int:
        return sum(len(item) for item in self.sequences)

    def __getitem__(self, index: Union[slice, int]) -> Any:
        if isinstance(index, slice):
            return SliceView(self,
                             start=index.start,
                             stop=index.stop,
                             step=index.step)

        length = len(self)
        ipos = index if index >= 0 else length + index

        for item in self.sequences:
            if ipos < len(item):
                return item if not isinstance(item, Iterable) else item[ipos]
            ipos -= len(item)

        raise IndexError(f'Index out of range ({index})')

    def __repr__(self) -> str:
        params = ', '.join(f'{i!r}' for i in self.sequences)
        return f'{self.__class__.__name__}({params})'

    def __add__(self, other) -> 'ChainSequence':
        return ChainSequence(*self.sequences, other)

    def __iadd__(self, other) -> 'ChainSequence':
        self.sequences.append(other)
        return self
