class SliceView:
    def __init__(self, it, *, start=None, stop=None, step=None) -> None:
        start, stop, step = slice(start, stop, step).indices(len(it))
        self._data = it
        self._range = range(start, stop, step)

    def __len__(self):
        return len(self._range)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SliceView(self,
                             start=index.start,
                             stop=index.stop,
                             step=index.step)
        return self._data[self._range[index]]
