def all_same(lst):
    if not lst:
        return True
    i = iter(lst)
    first = next(i)
    return all(first == match for match in i)
