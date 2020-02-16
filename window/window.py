def window(elements, n):
    entries = []
    if n > 0:
        done = False
        element_iterator = iter(elements)
        while not done:
            try:
                while len(entries) < n:
                    entries.append(next(element_iterator))
                yield tuple(entries)
                entries = entries[1:]
            except StopIteration:
                done = True
    else:
        return []
