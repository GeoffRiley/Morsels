import math
import cmath
from decimal import Decimal, ROUND_DOWN, getcontext


def isint(val):
    return int(val) == val


def is_perfect_square(num, *, complex=False):
    if complex:
        complex_num_root = cmath.sqrt(num)
        return isint(complex_num_root.real) and isint(complex_num_root.imag)
    else:
        if num <= 0:
            return False
        if int(float(num)) == num:
            return int(math.sqrt(num)) ** 2 == num
        else:
            getcontext().rounding = ROUND_DOWN
            getcontext().prec = 60
            return Decimal(num).sqrt().quantize(1) ** Decimal(2) == num
