import inspect
import pdb
from functools import wraps
from typing import Callable


def create_arglist(args, kwargs):
    return ', '.join((*(repr(x) for x in args), *(f'{x[0]}={x[1]!r}'
                                                  for x in kwargs.items())))


def debug_calls(*db_args, **db_kwargs):
    def _debug_calls(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            caller = inspect.stack()[1]
            arglist = create_arglist(args, kwargs)
            print(f'{func.__name__}({arglist}) '
                  f'called by {caller.function} '
                  f'in file "{caller.filename}" '
                  f'on line {caller.lineno}')
            if set_break:
                # return func(*args, **kwargs)
                if not wrapper.condition:
                    wrapper.condition = input(f'Debug {func.__name__} when?')

                # NOTE: eval() is insecure and should not be used in live systems
                if eval(wrapper.condition, {},
                        sig.bind(*args, **kwargs).arguments):
                    print(f'Condition met: {wrapper.condition}')
                    return pdb.runcall(func, *args, **kwargs)

                print(f'Condition not met: {wrapper.condition}')
            return func(*args, **kwargs)

        wrapper.condition = None
        return wrapper

    if db_kwargs and 'set_break' in db_kwargs:
        set_break = db_kwargs['set_break']
    else:
        set_break = False

    if len(db_args) == 1 and callable(db_args[0]):
        return _debug_calls(db_args[0])
    return _debug_calls
