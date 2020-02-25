class suppress(object):
    def __init__(self, *execption_types):
        self._exceptions_to_suppress = execption_types

    def __enter__(self):
        self.exc_val = None
        self.exc_tb = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exc_val = exc_val
        self.exc_tb = exc_tb
        if exc_type:
            if exc_type is self._exceptions_to_suppress \
                    or issubclass(exc_type, self._exceptions_to_suppress):
                return True
        return None

    @property
    def exception(self):
        return self.exc_val

    @property
    def traceback(self):
        return self.exc_tb

    def __call__(self, func):
        def wrapper(*args, **kwds):
            with self:
                return func(*args, **kwds)

        return wrapper
