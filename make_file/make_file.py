import tempfile


class make_file:
    def __init__(self,
                 contents: str = None,
                 directory: str = None,
                 **kwargs) -> None:
        self.contents = contents
        self.directory = directory
        self.kwargs = kwargs
        if 'mode' not in kwargs:
            self.kwargs['mode'] = 'wt'

    def __enter__(self) -> str:
        self.tmp = tempfile.NamedTemporaryFile(dir=self.directory,
                                               **self.kwargs)
        if self.contents is not None:
            with open(self.tmp.name, **self.kwargs) as tmp:
                tmp.write(self.contents)
        return self.tmp.name

    def __exit__(self, *args):
        self.tmp.close()
