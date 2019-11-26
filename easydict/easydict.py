from collections import UserDict


class EasyDict(UserDict):
    def __init__(self, *args, **kwargs) :
        init_dict = dict()
        if 'normalize' in kwargs.keys():
            self._normalize = str(kwargs.pop('normalize')).lower() == 'true'
        else:
            self._normalize = False
        for arg in args:
            if isinstance(arg, dict) or isinstance(arg, tuple):
                init_dict.update(arg)
        init_dict.update({k: v for k, v in kwargs.items()})
        super().__init__(init_dict)

    def __getitem__(self, key):
        key = self._normalize_key(key)
        return self.__dict__[key]

    def __setitem__(self, key, value):
        key = self._normalize_key(key)
        self.__dict__[key] = value

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def _normalize_key(self, key):
        if self._normalize:
            key = key.replace(' ', '_').replace('-', '_')
        return key
