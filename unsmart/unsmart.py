import argparse
import re

MAPPING = {
    '“': '"',
    '”': '"',
    '‘': "'",
    '’': "'",
    '–': '-',
    '—': '--',
    '…': '...'
}


def _do_sub(match):
    return MAPPING[match.group(0)]


def parser_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType('rt', encoding='UTF-8'))
    return parser.parse_args()


def main():
    args = parser_command_line()

    with args.infile as inf:
        text: str
        text = inf.read()

        # chars_a = '“”‘’'
        # chars_b = '""' + "''"
        # trans_table = text.maketrans(chars_a, chars_b)
        # text = text.translate(trans_table)
        # text = re.sub('–', '-', text)
        # text = re.sub('—', '--', text)
        # text = re.sub('…', '...', text)

        text = re.sub(fr'[{"".join(MAPPING.keys())}]', _do_sub, text)

        text = '\n'.join(l.rstrip() for l in text.splitlines(keepends=False))

        print(text, end='')


if __name__ == '__main__':
    main()
