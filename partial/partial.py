from typing import Any, Callable

SKIP = object()


class partial:
    func: Callable
    args: tuple
    kwargs: dict

    def __new__(cls, func: Callable, *args: Any, **kwargs: Any):
        self = super().__new__(cls)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        new_args = list(args)
        combined_args = []
        for arg in self.args:
            if arg is SKIP:
                if new_args:
                    arg = new_args.pop(0)
                else:
                    raise TypeError('Not enough positional arguments given')
            combined_args.append(arg)
        combined_args.extend(new_args)
        combined_kwargs = {**self.kwargs, **kwargs}
        return self.func(*combined_args, **combined_kwargs)

    def partial(self, *args: Any, **kwargs: Any) -> Any:
        combined_args = self.args + args
        combined_kwargs = self.kwargs.copy()
        combined_kwargs.update(kwargs)
        return partial(self.func, *combined_args, **combined_kwargs)

    def __repr__(self) -> str:
        arglist = ', '.join([
            self.func.__name__, *[repr(a) for a in self.args],
            *[f'{k}={repr(v)}' for k, v in self.kwargs.items()]
        ])
        return f'<{arglist}>'
