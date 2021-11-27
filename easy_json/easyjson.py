import json
from collections.abc import Mapping


class MyJSONObject(Mapping):
    def __init__(self, json_dict: dict) -> None:
        self._json = json_dict

    def __getitem__(self, ndx):
        # print(type(ndx), ndx)
        if ndx is Ellipsis:
            return self._json.values
        if isinstance(ndx, tuple):
            return MyJSONObject({x: self._json[x] for x in ndx})
        return self._json[ndx]

    def __iter__(self):
        return iter(self._json)

    def __len__(self) -> int:
        return len(self._json)

    def __getattr__(self, ndx):
        return self[ndx]

    def __repr__(self) -> str:
        return repr(self._json)


def parse(js_data: str):
    return json.loads(js_data, object_hook=MyJSONObject)
