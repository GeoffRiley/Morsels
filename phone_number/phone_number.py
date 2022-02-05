import re

PHONE_MATCH = re.compile(
    r'^             '
    r'\s*\(?\s*     '
    r'(\d{3})       '
    r'\s*[-).]*\s*  '
    r'(\d{3})       '
    r'\s*[-.]*\s*   '
    r'(\d{4})       '
    r'\s*$          ', re.IGNORECASE | re.VERBOSE)


class PhoneNumber:
    __slots__ = ('_number', )

    def __init__(self, number: str) -> None:
        parts = PHONE_MATCH.match(number)
        if not (parts and len(parts.groups()) == 3):
            raise ValueError('Invalid phone number')
        self._number = ''.join(parts.groups())

    @property
    def area_code(self) -> str:
        return self._number[:3]

    @property
    def prefix(self) -> str:
        return self._number[3:6]

    @property
    def line_number(self) -> str:
        return self._number[-4:]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._number!r})'

    def __str__(self) -> str:
        return f'{self.area_code}-{self.prefix}-{self.line_number}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PhoneNumber):
            return NotImplemented
        return self._number == other._number

    def __hash__(self) -> int:
        return hash(self._number)

    def __format__(self, fmt: str) -> str:
        pfx = ''
        if not fmt:
            fmt = '-'
        elif fmt == '(':
            return f'({self.area_code}) {self.prefix}-{self.line_number}'
        elif fmt[0] == '+':
            pfx = '+1'
            fmt = fmt[1:]
        gap = fmt if len(fmt) < 2 else fmt[1] + fmt
        if pfx:
            pfx += gap
        return f'{pfx}{self.area_code}{gap}{self.prefix}' \
            f'{gap}{self.line_number}'
