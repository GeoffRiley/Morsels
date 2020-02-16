from itertools import islice

NOFILL = object()


def chunked(elements, n, *, fill=NOFILL):
    iterator = iter(elements)
    done = False
    while not done:
        res = tuple(islice(iterator, n))
        if len(res) == 0:
            done = True
        else:
            if fill is not NOFILL:
                yield (res + tuple([fill] * (n - len(res))))
            else:
                yield res
