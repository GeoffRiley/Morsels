import argparse
import configparser
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

    conf = configparser.ConfigParser()
    conf.read(args.infile.name)

    results, sections = [], []
    header = ['header']

    for s in conf.sections():
        sections.append(s)
        for v, p in conf.items(s):
            if v not in header:
                header.append(v)

            results.append(('header', s, v, p))

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
