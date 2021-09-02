import argparse
import regex as re
import csv


def get_cmdline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile",
                        type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument("outfile",
                        type=argparse.FileType('w', encoding='UTF-8'))
    parser.add_argument('--collapsed', action='store_true', default=False)
    return parser.parse_args()


def main():
    args = get_cmdline_args()

    text = args.infile.read()

    section, results, sections = '', [], []
    header = ['header']

    matcher = re.compile(
        r'^(?:\[(?P<section>.*)\]|(?P<var>[^[= ]+) ?= ?(?P<param>[^[]+?))$',
        re.MULTILINE)

    entries = [m.groupdict() for m in matcher.finditer(text)]

    for entry in entries:
        if entry['section']:
            section = entry['section']
            if section not in sections:
                sections.append(section)
        else:
            v, p = entry['var'], entry['param']

            if v not in header:
                header.append(v)

            results.append(('header', section, v, p))

    if args.collapsed:
        reorder = dict({s: dict() for s in sections})

        for _, s, v, p in results:
            reorder[s][v] = p

        results2 = [header]

        for s, params in reorder.items():
            results2.append([s, *[params[h] for h in header[1:]]])
    else:
        results2 = [[s, v, p] for _, s, v, p in results]

    csv_out = csv.writer(args.outfile)
    csv_out.writerows(results2)

    args.infile.close()
    args.outfile.close()


if __name__ == "__main__":
    main()
