from pathlib import Path
import os
import tempfile


class cd:
    def __init__(self, directory: Path = None) -> None:
        self.tmpdir = (directory is None)
        self.dest = directory

    def __enter__(self) -> 'cd':
        self.cwd = Path.cwd()
        if self.tmpdir:
            self.tempdirectory = tempfile.TemporaryDirectory()
        os.chdir(self.dest or self.tempdirectory.name)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
        os.chdir(self.cwd)
        if self.tmpdir:
            self.tempdirectory.cleanup()

    @property
    def previous(self) -> Path:
        return self.cwd

    @property
    def current(self) -> Path:
        return self.dest

    enter = __enter__

    def exit(self):
        self.__exit__(None, None, None)
