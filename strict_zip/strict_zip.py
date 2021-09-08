SENTINEL = object()


def strict_zip(*args):
    iters = [iter(x) for x in args]
    if len(iters):
        while True:
            result = tuple(next(x, SENTINEL) for x in iters)
            if SENTINEL in result:
                if any(x != SENTINEL for x in result):
                    raise ValueError('Value out of range')
                break
            yield result
    return []
