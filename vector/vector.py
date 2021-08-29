class Vector(object):
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__()
        object.__setattr__(self, 'x', x)
        object.__setattr__(self, 'y', y)
        object.__setattr__(self, 'z', z)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Vector):
            raise TypeError(
                f'{self.__class__.__name__} cannot be compared with '
                f'{o.__class__.__name__}')
        return (self.x == o.x and self.y == o.y and self.z == o.z)

    def __ne__(self, o: object) -> bool:
        if not isinstance(o, Vector):
            raise TypeError(
                f'{self.__class__.__name__} cannot be compared with '
                f'{o.__class__.__name__}')
        return not (self.x == o.x and self.y == o.y and self.z == o.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, o: object) -> 'Vector':
        if not isinstance(o, Vector):
            raise TypeError(f'{o.__class__.__name__} cannot be added to '
                            f'{self.__class__.__name__}')
        return Vector(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o: object) -> 'Vector':
        if not isinstance(o, Vector):
            raise TypeError(
                f'{o.__class__.__name__} cannot be subtracted from '
                f'{self.__class__.__name__}')
        return Vector(self.x - o.x, self.y - o.y, self.z - o.z)

    def __rsub__(self, o: object) -> 'Vector':
        if not isinstance(o, Vector):
            raise TypeError(
                f'{self.__class__.__name__} cannot be subtracted from '
                f'{o.__class__.__name__}')
        return Vector(o.x - self.x, o.y - self.y, o.z - self.z)

    def __mul__(self, o: object) -> 'Vector':
        if not isinstance(o, (float, int)):
            raise TypeError(
                f'{self.__class__.__name__} cannot be multiplied by '
                f'{o.__class__.__name__}')
        return Vector(self.x * o, self.y * o, self.z * o)

    def __rmul__(self, o: object) -> 'Vector':
        if not isinstance(o, (float, int)):
            raise TypeError(f'{o.__class__.__name__} cannot be multiplied by '
                            f'{self.__class__.__name__}')
        return Vector(o * self.x, o * self.y, o * self.z)

    def __truediv__(self, o: object) -> 'Vector':
        if not isinstance(o, (float, int)):
            raise TypeError(f'{self.__class__.__name__} cannot be divided by '
                            f'{o.__class__.__name__}')
        return Vector(self.x / o, self.y / o, self.z / o)

    def __rtruediv__(self, o: object) -> 'Vector':
        if not isinstance(o, (float, int)):
            raise TypeError(f'{o.__class__.__name__} cannot be divided by '
                            f'{self.__class__.__name__}')
        return Vector(o / self.x, o / self.y, o / self.z)

    def __setattr__(self, *args) -> None:
        raise AttributeError(f'{self.__class__.__name__} is Immutable')

    __delattr__ = __setattr__
