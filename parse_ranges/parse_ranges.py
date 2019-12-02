def parse_ranges(range_list: str) -> list:
    parts = range_list.split(',')
    for part in parts:
        if '-' in part:
            f, t = part.split('-')
            if t.startswith('>'):
                yield int(f)
            else:
                yield from range(int(f), int(t)+1)
        else:
            yield int(part)
