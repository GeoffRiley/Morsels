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


def int_to_roman(value: int) -> str:
    result = ''
    for k, v in ROMAN_VALUES:
        while value >= v:
            result += k
            value -= v
    return result


def roman_to_int(string: str) -> int:
    result = 0
    for k, v in ROMAN_VALUES:
        while string.startswith(k):
            result += v
            string = string[len(k):]
    if string:
        raise ValueError
    return result
