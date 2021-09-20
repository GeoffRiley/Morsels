from itertools import chain, islice, repeat
from typing import Sequence

SEMAPHORE = object()


def _gen_list(iseq: Sequence, ret_count: int, sub_len: int,
              sub_boost_count: int):
    for _ in range(ret_count):
        yield islice(iseq, 0, sub_len + (1 if sub_boost_count > 0 else 0))
        sub_boost_count -= 1


def divide(*args, **kwargs):
    if len(args) > 2:
        raise TypeError
    elif len(args) == 2:
        seq, n = args
    else:
        seq = args[0]
        n = kwargs.get('n')

    seq = list(seq)
    length = kwargs.get('length', len(seq))
    fill = kwargs.get('fill', SEMAPHORE)

    c, r = divmod(length, n)
    if fill is not SEMAPHORE:
        r = n

    iseq = iter(chain(seq, repeat(fill)))

    return _gen_list(iseq, n, c, r)
