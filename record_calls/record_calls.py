import functools
from typing import Any, Dict, List, NamedTuple, Union
from dataclasses import dataclass

NO_RETURN = object()


@dataclass
class FunctionRecord(object):
    args: List[Any]
    kwargs: Dict[str, Any]
    return_value: Any = NO_RETURN
    exception: Union[Exception, None] = None


def record_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        index = len(wrapper.calls)
        wrapper.calls.append(FunctionRecord(args, kwargs))
        try:
            rv = func(*args, **kwargs)
            wrapper.calls[index].return_value = rv
        except Exception as err:
            wrapper.calls[index].exception = err
            raise
        return rv

    wrapper.call_count = 0
    wrapper.calls = []
    return wrapper
