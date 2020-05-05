from collections import UserDict


class PermaDict(UserDict):
    def __init__(self, *args, silent=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.silent = silent

    def __setitem__(self, key, value):
        if key in self:
            if not self.silent:
                raise KeyError(f"'{key}' is already in dictionary")
        else:
            super().__setitem__(key, value)

    def force_set(self, key, value):
        super().__setitem__(key, value)

    def update(self, *args, force=False, **kwargs):
        if not force:
            super().update(*args, **kwargs)
        else:
            d = dict(*args, **kwargs)
            for k, v in d.items():
                self.force_set(k, v)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.data.__repr__()})'
