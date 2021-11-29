import json
from typing import Union

ellipsis = type(Ellipsis)


class MyJSONObject:
    def __init__(self, json_dict: Union[list, dict]) -> None:
        self._json = json_dict
        super().__init__()

    def __getitem__(self, ndx: Union[ellipsis, int, slice, str]):
        if ndx is Ellipsis:
            return MyJSONObject(self._json)
        if isinstance(ndx, tuple):
            return MyJSONObject({x: self._json[x] for x in ndx})
        if isinstance(self._json, list):
            try:
                value = MyJSONObject([x[ndx] for x in self._json])
            except KeyError:
                value = self._json[ndx]
        else:
            value = self._json[ndx]
        return value if not isinstance(value, list) else MyJSONObject(value)

    def __iter__(self):
        return iter(self._json)

    def __getattr__(self, ndx):
        return self[ndx]

    def __repr__(self) -> str:
        return repr(self._json)

    def __eq__(self, __o: object) -> bool:
        return (self._json) == (__o)

    def keys(self) -> list:
        return self._json.keys()


def parse(js_data: str):
    return MyJSONObject(json.loads(js_data, object_hook=MyJSONObject))
