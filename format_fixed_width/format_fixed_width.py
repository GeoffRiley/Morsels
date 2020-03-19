from itertools import zip_longest


def format_fixed_width(list_var, padding=2, widths=None, alignments=None):
    if len(list_var) == 0:
        return ""
    if widths is None:
        widths = [len(max(row, key=len)) for row in zip(*list_var)]
    if alignments is None:
        alignments = ['L' for _ in list_var[0]]
    result_strings = []
    for col, (_, width, alignment) in enumerate(zip(list_var[0], widths, alignments)):
        new_result_strings = []
        for line, the_list in zip_longest(result_strings, list_var, fillvalue=''):
            if alignment == 'L':
                line += the_list[col].ljust(width)
            else:
                line += the_list[col].rjust(width)
            new_result_strings.append(line + (' ' * padding))
        result_strings = new_result_strings
    return '\n'.join(s.rstrip() for s in result_strings)
