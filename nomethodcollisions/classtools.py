from collections import UserDict
from typing import Any, Mapping, Tuple


class MetaNoMethodCollisions(type):
    """
    A 'metaclass' controller that watches over the methods and properties added
    into the classes dictionary and raises an error if any methods are
    redefined.  This has to be introduced to a subclass by defining it as a
    metaclass in the descendancy declaration.
    """
    @classmethod
    def __prepare__(metacls, __name: str, __bases: Tuple[type, ...],
                    **kwds) -> Mapping[str, Any]:
        class _NoMethodCollisions(UserDict):
            """
            This is a special dictionary class for the NoMethodCollision class
            that keeps a note of when a key is re-assigned.
            """
            def __init__(self, *args, **kwargs) -> None:
                self.seen = set()
                super().__init__(*args, **kwargs)

            def __setitem__(self, key: Any, item: Any) -> None:
                if key in self.data:
                    self.seen.add(key)
                self.data[key] = item

        return _NoMethodCollisions()

    def __new__(cls, name: str, bases: Tuple[type, ...],
                namespace) -> 'MetaNoMethodCollisions':
        for key in namespace.seen:
            value = namespace[key]
            if (not isinstance(value, property)
                    and (callable(value) or hasattr(value, '__get__'))):
                raise TypeError("Method collision")
        return super().__new__(cls, name, bases, dict(namespace))


class NoMethodCollisions(metaclass=MetaNoMethodCollisions):
    """
    This is purely a class to descend from to ensure that the metaclass
    properies get set up. I have no idea why I couldn't get it to work with
    the functionality embedded!
    """
    pass
