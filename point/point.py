class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, i: int):
        self._x = i

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, i: int):
        self._y = i

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, i: int):
        self._z = i

    def _tuple(self):
        return [self.x, self.y, self.z]

    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})'

    def __eq__(self, other):
        if not isinstance(other, Point):
            raise TypeError('Can only compare points')
        return self._tuple() == other._tuple()

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError('Can only add two points')
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError('Can only add two points')
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError('Point can only be multiplied by a number')
        return Point(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)
