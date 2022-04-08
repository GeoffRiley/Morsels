"""List comprehension exercises"""

import itertools
from typing import List


def get_vowel_names(names: List[str]):
    """Return a list containing all names given that start with a vowel."""
    return [x for x in names if x[0].lower() in 'aeiou']


def flatten(matrix: List[list]):
    """Return a flattened version of the given 2-D matrix (list-of-lists)."""
    return [item for row in matrix for item in row]


def matrix_from_string(lines: str):
    """Convert rows of numbers to list of lists."""
    return [[int(x) for x in line.split()] for line in lines.splitlines()]


def power_list(lst):
    """Return a list that contains each number raised to the i-th power."""
    return [n**x for x, n in enumerate(lst)]


def matrix_add(mat1, mat2):
    """Add corresponding numbers in given 2-D matrices."""
    # wid = len(mat1)
    # hei = len(mat1[0])
    # res = [[0 for _ in range(hei)] for _ in range(wid)]
    # for w, h in itertools.product(range(wid), range(hei)):
    #     res[w][h] = mat1[w][h] + mat2[w][h]
    # return res
    return [[n + m for n, m in zip(row1, row2)]
            for row1, row2 in zip(mat1, mat2)]


def identity(size):
    """Return an identity matrix of size x size."""
    return [[int(x == y) for x in range(size)] for y in range(size)]


def triples(limit):
    """Return list of Pythagorean triples less than input num."""
    return [(a, b, c)
            for a, b, c in itertools.combinations(range(1, limit), 3)
            if (a**2) + (b**2) == (c**2)]
