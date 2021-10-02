class PiecewiseRange:
    def __init__(self, ranges_string: str) -> None:

        ranges = []
        length = 0
        for part in ranges_string.split(','):
            if '-' in part:
                part_from, part_to = map(int, part.strip().split('-'))
                ranges.append((part_from, part_to))
                length += part_to - part_from + 1
            else:
                ranges.append(int(part.strip()))
                length += 1

        self.ranges = ranges
        self.length = length

        self._collapse_()

    def __iter__(self):
        for part in self.ranges:
            if isinstance(part, int):
                yield part
            else:
                part_from, part_to = part
                yield from range(part_from, part_to + 1)

    def __len__(self):
        return self.length

    def __getitem__(self, ndx: int) -> int:
        if ndx < 0:
            ndx += len(self)

        for part in self.ranges:
            if isinstance(part, int):
                if ndx == 0:
                    return part
                ndx -= 1
            else:
                part_from, part_to = part
                part_len = part_to - part_from
                if ndx <= part_len:
                    return range(part_from, part_to + 1)[ndx]
                ndx -= part_len + 1
        raise IndexError('index not found')

    def __repr__(self) -> str:
        out = []
        for part in self.ranges:
            if isinstance(part, int):
                out.append(f'{part}')
            else:
                part_from, part_to = part
                out.append(f'{part_from}-{part_to}')
        return f"{self.__class__.__name__}('{','.join(out)}')"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.ranges == o.ranges

    def _collapse_(self):
        reduced = []
        last_part = None
        for part in self.ranges:

            if last_part is None:
                last_part = part

            elif isinstance(part, int):
                if isinstance(last_part, int) and part == last_part + 1:
                    last_part = (last_part, part)
                elif isinstance(last_part, tuple) and part == last_part[1] + 1:
                    last_part = (last_part[0], part)
                else:
                    reduced.append(last_part)
                    last_part = part

            elif isinstance(last_part, int) and part[0] == last_part + 1:
                last_part = (last_part, part[1])
            elif isinstance(last_part, tuple) and part[0] == last_part[1] + 1:
                last_part = (last_part[0], part[1])
            else:
                reduced.append(last_part)
                last_part = part
        if last_part is not None:
            reduced.append(last_part)
        self.ranges = reduced
