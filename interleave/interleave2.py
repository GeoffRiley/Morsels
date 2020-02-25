from itertools import zip_longest


def interleave(*lists):
    res = []
    SENTINAL = object()
    for a in zip_longest(*lists, fillvalue=SENTINAL):
        for b in a:
            if b is not SENTINAL:
                yield b
