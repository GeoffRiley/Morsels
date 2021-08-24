from typing import Any, Dict, List

SEMAPHORE = object()


def _pluck_one(data: Dict[str, dict], path: str, sep: str, default: Any) -> Any:
    path_seq = path.split(sep)
    current_data = data
    while len(path_seq):
        path_element = path_seq.pop(0)
        for k, v in current_data.items():
            if k == path_element:
                current_data = v
                break
        else:
            if default is not SEMAPHORE:
                return default
            else:
                raise KeyError('path not found')
    return current_data


def pluck(data: Dict[str, dict], *paths: List[str], sep: str = '.', default: Any = SEMAPHORE) -> Any:
    result = tuple()
    for path in paths:
        result += ((_pluck_one(data, path, sep, default)),)

    return result[0] if len(result) == 1 else result
