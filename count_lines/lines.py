"""line.py

    Calculate stats about the contents of specified textural files.

    count_lines(a_path [, extensions])
        a_path is the directory name containing the files to be examined
            (recursive into subdirectories)
        extensions is a list of filename extensions to be examined, this
            has a default list of ['py', 'md', 'html', 'js']

    The returned value is a hybrid dictionary object containing entries for
    each of the locate extensions with a corresponding value of a line_stat.
    The line_stat structure holds a count of files, the number of lines within
    those files and the number of non-blank lines therein.
    The hybrid dictionary additionally has a list named 'ignored' that holds
    all the filenames that either do not match the required extensions, are
    not readable, or have some unexpected error associated with them.
"""
from collections import UserDict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Reason(Enum):
    """Reasons for ignoring a filename"""
    EXTENSION = 1
    PERMISSION = 2
    OTHER = 3


class IgnoreDict(UserDict):
    """Add in an extra 'ignored' list alongside the regular dictionary"""
    def __init__(self):
        super().__init__()
        self.ignored = []


@dataclass
class LineStat():
    """Hold the stats for a set of files"""
    files: int = 0
    lines: int = 0
    non_blank: int = 0


def count_lines(a_path: str, extensions: list = None) -> IgnoreDict:
    """
    Scan a_path for any files with appropriate extension and
    assemble an appropriate summary.
    """
    if not extensions:
        extensions = ['py', 'md', 'html', 'js']
    result = IgnoreDict()
    path = Path(a_path)

    for file in path.glob('**/*'):
        if file.is_file():
            if (ext := file.suffix.lstrip('.')) in extensions:
                try:
                    lines = file.read_text().splitlines(keepends=False)
                    if ext not in result.keys():
                        result[ext] = LineStat()
                    result[ext].files += 1
                    result[ext].lines += len(lines)
                    result[ext].non_blank += len(
                        [a for a in lines if a.strip()])
                except OSError:
                    result.ignored.append((file.name, Reason.PERMISSION))
                except Exception:
                    result.ignored.append((file.name, Reason.OTHER))
            else:
                result.ignored.append((file.name, Reason.EXTENSION))

    return result
