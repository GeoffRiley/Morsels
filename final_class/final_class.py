class UnsubclassableType(type):
    def __new__(cls, name, bases, classdict):
        for base in bases:
            if isinstance(base, UnsubclassableType):
                raise TypeError(
                    f"'{cls.__name__}' is an unacceptable base type")
        return super().__new__(cls, name, bases, classdict)


class Unsubclassable(metaclass=UnsubclassableType):
    pass


def final_class(cls):
    @classmethod
    def deny_subclass(subclass):
        raise TypeError(
            f"Class '{subclass.__name__} cannot subclass {cls.__name__}")

    cls.__init_subclass__ = deny_subclass
    return cls
