from operator import length_hint


def total_length(*args, use_hints: bool = False) -> int:
    def _len(o: object) -> int:
        _l: int = 0
        try:
            _l = len(o)
        except TypeError:
            if use_hints:
                _l = length_hint(o)
                if _l == 0:
                    _l = len(list(o))
            else:
                _l = len(list(o))

        return _l

    return sum([_len(a) for a in args])
