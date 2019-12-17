import types


def deep_add(lst, start=0):
    s = flatten(lst)
    res = start
    for i in s:
        res += i
    return res


def flatten(lst):
    s = []
    if isinstance(lst, (list, tuple, set, types.GeneratorType)):
        for l in lst:
            if isinstance(l, (list, tuple, set, types.GeneratorType)):
                for m in flatten(l):
                    s.append(m)
            else:
                s.append(l)
    else:
        s.append(list)
    return s
