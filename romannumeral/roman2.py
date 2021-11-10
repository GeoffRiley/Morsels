from functools import total_ordering

ROMAN_VALUES = [
    ['M', 1000],
    ['CM', 900],
    ['D', 500],
    ['CD', 400],
    ['C', 100],
    ['XC', 90],
    ['L', 50],
    ['XL', 40],
    ['X', 10],
    ['IX', 9],
    ['V', 5],
    ['IV', 4],
    ['I', 1],
]


@total_ordering
class RomanNumeral:
    def __init__(self, numeral: str = None) -> None:
        self.numeral = numeral

    def __int__(self) -> int:
        return self.roman_to_int()

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.numeral!r})'

    def __str__(self) -> str:
        return self.numeral

    def __add__(self, other: object) -> 'RomanNumeral':
        try:
            i = int(other)
        except Exception:
            return NotImplemented
        return RomanNumeral.from_int(int(self) + i)

    def __eq__(self, other: object) -> bool:
        try:
            i = int(other)
        except Exception:
            if isinstance(other, str):
                i = int(RomanNumeral(other))
            else:
                return NotImplemented
        return int(self) == i

    def __lt__(self, other: object) -> bool:
        try:
            i = int(other)
        except Exception:
            return NotImplemented
        return int(self) < i

    @classmethod
    def from_int(cls, value: int) -> 'RomanNumeral':
        return cls(cls.int_to_roman(value))

    @classmethod
    def int_to_roman(cls, value: int) -> str:
        result = ''
        for k, v in ROMAN_VALUES:
            while value >= v:
                result += k
                value -= v
        return result

    def roman_to_int(self) -> int:
        string = self.numeral
        result = 0
        for k, v in ROMAN_VALUES:
            while string.startswith(k):
                result += v
                string = string[len(k):]
        if string:
            raise ValueError
        return result
