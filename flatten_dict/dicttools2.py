from typing import Any, Callable, Dict


def flatten_dict(arr: Dict[Any, dict],
                 *,
                 sep: str = '_',
                 key_maker: Callable = None) -> dict:
    def default_key_maker(k: list):
        return sep.join(str(i) for i in k)

    if key_maker is None:
        key_maker = default_key_maker

    result = {}
    working = [([k], v) for k, v in arr.items()]
    while working:
        (k, v) = working.pop(0)
        if isinstance(v, dict):
            if v:
                working.extend([(k + [k1], v1) for k1, v1 in v.items()])
        else:
            if len(k) > 1:
                k1 = key_maker(k)
                if isinstance(k1, list):
                    k1 = tuple(k1)
                result[k1] = v
            else:
                result[k[0]] = v

    return result
