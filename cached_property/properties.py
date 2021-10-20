SEMAPHORE = object()


class cached_property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset if fset is not None else self._dum_dum_clear
        self.fdel = fdel if fset is not None else self._dum_dum_clear
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._current_value = {}

    def _dum_dum_clear(self, obj, value=SEMAPHORE):
        self._current_value[hash(obj)] = value

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        if self._current_value.get(hash(obj), SEMAPHORE) is SEMAPHORE:
            self._current_value[hash(obj)] = self.fget(obj)
        return self._current_value[hash(obj)]

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self._current_value[hash(obj)] = SEMAPHORE
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self._current_value[hash(obj)] = SEMAPHORE
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
