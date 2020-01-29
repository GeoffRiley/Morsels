def format_ranges(arr):
    arr = sorted(arr)
    res = []
    base = arr.pop(0)
    nxt = base + 1
    runon = False
    while len(arr) > 0:
        if nxt in arr:
            arr.remove(nxt)
            nxt += 1
            runon = True
            continue
        if runon:
            res.append((base, nxt - 1))
            runon = False
        else:
            res.append((base, base))
        base = arr.pop(0)
        nxt = base + 1
    if runon:
        res.append((base, nxt - 1))
    else:
        res.append((base, base))
    return ','.join(f'{t[0]}-{t[1]}' if t[0] != t[1] else str(t[0]) for t in sorted(res))
