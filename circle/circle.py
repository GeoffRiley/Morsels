import math


class Circle:
    def __init__(self, rad=1):
        self.radius = rad

    def __str__(self):
        return f'{self.__class__.__name__}({self.radius})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.radius})'

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, rad):
        if rad < 0:
            raise ValueError('Radius cannot be negative')
        self._radius = rad

    @property
    def diameter(self):
        return self.radius * 2

    @diameter.setter
    def diameter(self, dia):
        self.radius = dia / 2

    @property
    def area(self):
        return math.pi * (self.radius ** 2)
