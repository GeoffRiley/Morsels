from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, version):
        self._parts = [int(p) for p in version.split('.')]
        if not (0 < len(self._parts) <= 3):
            raise ValueError("Version must have 1-3 numeric parts")
        self._parts += [0] * (3 - len(self._parts))

    def __eq__(self, other):
        if isinstance(other, Version):
            return self._parts == other._parts
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Version):
            return self._parts < other._parts
        return NotImplemented

    def __str__(self):
        return "{0}.{1}.{2}".format(*self._parts)

    def __repr__(self):
        return "Version({!r})".format(str(self))
