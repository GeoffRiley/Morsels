def compact(it):
    first = True
    prev = None
    for i in it:
        if first or i != prev:
            first = False
            prev = i
            yield i
