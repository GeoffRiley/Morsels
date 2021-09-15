import csv
from typing import List, Optional, Union
from collections import namedtuple


class FancyReader:
    def __init__(self,
                 lines: List[str],
                 fieldnames: Optional[List[str]] = None,
                 dialect: Union[str, csv.Dialect] = 'excel') -> None:
        self.reader = csv.reader(iter(lines), dialect=dialect)
        if fieldnames is None:
            self.fieldnames = next(self.reader)
            self.line_num = 1
        else:
            self.fieldnames = fieldnames
            self.line_num = 0
        self.current = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            self.current = namedtuple('Row', self.fieldnames)

        self.line_num += 1
        return self.current(*next(self.reader))
