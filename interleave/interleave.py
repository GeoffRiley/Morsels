def interleave(list_a, list_b):
    res = []
    for a, b in zip(list_a, list_b):
        yield a
        yield b
