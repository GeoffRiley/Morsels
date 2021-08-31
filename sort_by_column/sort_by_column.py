"""Sort csv by column

Given the filename of a csv file and the number of one or more columns,
print the csv file sorted by the contents of the indicated
column(s).

    usage: sort_by_column.py [-h] [--with-header] filename col_no [col_no ...]
"""
import argparse
import csv
from sys import stdout


def sort_csv_by_column(filename: str, columns: int, header: bool):
    def sort_value(a):
        key = []
        for col in columns:
            c, *t = col.split(':')
            if len(t) == 0 or t[0] == 'str':
                key.append(a[int(c)])
            elif t[0] == 'num':
                key.append(int(a[int(c)]))
            else:
                raise KeyError('Sort type must be blank (or str) or num')
        return tuple(key)

    with open(filename, 'rt', newline='') as csv_file:
        dialect = 'excel'
        csv_file.seek(0)
        csv_lines = [row for row in csv.reader(csv_file, dialect=dialect)]
        if header:
            head = csv_lines.pop(0)
        sorted_csv = sorted(csv_lines, key=sort_value)
        csv_out = csv.writer(stdout, dialect=dialect)
        if header:
            csv_out.writerow(head)
        for row in sorted_csv:
            csv_out.writerow(row)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    parser.add_argument('col_no', type=str, nargs='+')
    parser.add_argument('--with-header', action='store_true')

    args = parser.parse_args()

    sort_csv_by_column(args.filename, args.col_no, args.with_header)


if __name__ == '__main__':

    main()
