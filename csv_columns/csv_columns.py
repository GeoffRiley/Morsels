import csv
from itertools import zip_longest


def csv_columns(csv_file, headers=None, missing=None):
    file_reader = csv.reader(csv_file)
    if headers:
        header = {h: list() for h in headers}
    else:
        header = {h: list() for h in next(file_reader)}
    for line in file_reader:
        for h, v in zip_longest(header, line, fillvalue=missing):
            header[h].append(v)
    return header
