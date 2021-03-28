from typing import List, Tuple, TextIO


def parse_fixed_width_file(text_file: TextIO, column_positions: List[Tuple[int, int]]):
    for line in text_file.read().splitlines():
        yield [line[a:b].strip() for a, b in column_positions]


def parse_columns(column_refs: str) -> List[Tuple[int, int]]:
    cols = column_refs.split(',')
    return [(int(a), int(b)) for a, b in [c.split(':') for c in cols]]


def quote(a_str: str) -> str:
    q = ''

    if {'"', ','}.intersection(set(a_str)):
        a_str = a_str.replace('"', '""', -1)
        q = '"'

    return f'{q}{a_str}{q}'


def main(args: List[str]):
    filenames = []
    cols = []
    for arg in args:
        if arg.startswith('--cols='):
            cols = parse_columns(arg[7:])
        else:
            filenames.append(arg)

    with open(filenames[0]) as text_file:
        lines = [','.join(quote(val) for val in col_vals) + '\n' for col_vals in
                 parse_fixed_width_file(text_file, cols)]
    with open(filenames[1], 'w') as csv_file:
        csv_file.writelines(lines)
