class alias(object):
    """Make a wrapper class to perform as an alias to a given name of a variable."""

    def __init__(self, name: str, write: bool = False):
        self._name = name
        self._write = write

    def __get__(self, instance, owner):
        """Act appropriately for class and instance variables."""
        if instance is None:
            return getattr(owner, self._name)
        else:
            return getattr(instance, self._name)

    def __set__(self, instance, value):
        """Disallow writing if write was not provided at creation."""
        if not self._write:
            raise AttributeError('Cannot assign to alias')
        setattr(instance, self._name, value)
