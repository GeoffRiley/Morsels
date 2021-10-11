import csv
from typing import List, Optional, Union


class BaseNameList:
    __slots__ = ()

    def __init__(self, *args) -> None:
        for k, v in zip(self.__slots__, args):
            self.__setattr__(k, v)

    def __iter__(self):
        return iter([self.__getattribute__(name) for name in self.__slots__])

    def __next__(self):
        yield from [self.__getattribute__(name) for name in self.__slots__]

    def __repr__(self) -> str:
        params = ', '.join(f'{name}={self.__getattribute__(name)!r}'
                           for name in self.__slots__)
        return f'{self.__class__.__name__}({params})'


class FancyReader:
    def __init__(self,
                 lines: List[str],
                 fieldnames: Optional[List[str]] = None,
                 dialect: Union[str, csv.Dialect] = 'excel',
                 **kwargs) -> None:
        self.reader = csv.reader(iter(lines), dialect=dialect, **kwargs)
        self._fieldnames = fieldnames
        self.line_num = 0
        self.Row = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.Row is None:
            self.Row = type('Row', (BaseNameList, ),
                            {'__slots__': self.fieldnames})
        self.line_num += 1
        return self.Row(*next(self.reader))

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            self._fieldnames = next(self.reader)
            self.line_num += 1
        return self._fieldnames
