import math

SUFFIXES = ' KMGT'


def format_bytes(value: int,
                 *,
                 bits: bool = False,
                 binary: bool = False) -> str:
    if value < 0:
        raise ValueError("Negative values not supported")

    divisor = 1024 if binary else 1000
    suffix_letter, trimmed_value = ('b', value * 8) if bits else ('B', value)
    suffix_index = math.floor(math.log(trimmed_value,
                                       divisor)) if trimmed_value > 0 else 0
    trimmed_value = round(trimmed_value / math.pow(divisor, suffix_index))

    presuffix_letter = 'i' if binary and suffix_index > 0 else ''
    suffix = f'{SUFFIXES[suffix_index]}{presuffix_letter}{suffix_letter}'

    return f'{trimmed_value}{suffix.strip()}'


def check_char(value_str: str, test_str: str) -> int:
    check = value_str[-1]
    if check in test_str:
        return test_str.index(check), value_str[:-1]
    return 0, value_str


def parse_bytes(value_str: str) -> int:
    bits_letter, value_str = check_char(value_str, ' bB')
    bin_flag, value_str = check_char(value_str, ' i')
    multiplier_letter, value_str = check_char(value_str, SUFFIXES)

    mult = 1024 if bin_flag == 1 else 1000
    value = math.floor(float(value_str) * (mult**multiplier_letter))
    if bits_letter == 1:
        value //= 8
    return value
