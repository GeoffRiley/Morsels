import _csv
import argparse
import csv
import sys


def main():
    parser = argparse.ArgumentParser(description="Fix csv files")
    parser.add_argument('infile', type=argparse.FileType('rt'))
    parser.add_argument('outfile', type=argparse.FileType('wt'))
    parser.add_argument('extras', nargs='*', help=argparse.SUPPRESS)
    parser.add_argument('--in-delimiter', action='store', nargs='?', type=str)
    parser.add_argument('--in-quote', action='store', default='"', type=str)
    args = parser.parse_args()
    try:
        if len(args.extras) > 0:
            raise BaseException('Too many arguments')
        if len(sys.argv) > 3:
            csv.register_dialect('in', delimiter=args.in_delimiter, quotechar=args.in_quote, quoting=_csv.QUOTE_MINIMAL)
            d_in = csv.get_dialect('in')
        else:
            sniffer = csv.Sniffer()
            d_in = sniffer.sniff(args.infile.read(1024))
            args.infile.seek(0)
        csv_in = csv.reader(args.infile, dialect=d_in)
        csv_out = csv.writer(args.outfile)
        for row in csv_in:
            csv_out.writerow(row)
    finally:
        args.infile.close()
        args.outfile.close()


if __name__ == "__main__":
    main()
