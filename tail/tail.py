def tail(seq, n):
    if n <= 0:
        return []
    return [i for i in seq][-n:]
