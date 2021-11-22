import argparse
import codecs
import sys


def check_codec_name(name: str) -> str:
    try:
        info = codecs.lookup(name)
    except LookupError:
        raise argparse.ArgumentTypeError
    return info.name


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('input', nargs='?', default='-')
    parse.add_argument('-o', '--output')
    parse.add_argument('-f',
                       '--from-code',
                       type=check_codec_name,
                       default=sys.getdefaultencoding())
    parse.add_argument('-t',
                       '--to-code',
                       type=check_codec_name,
                       default=sys.getdefaultencoding())
    parse.add_argument('-c', action='store_true', dest='ignore_errors')

    args = parse.parse_args()

    ignore = 'ignore' if args.ignore_errors else None

    if args.input == '-':
        sys.stdin.reconfigure(encoding=args.from_code, errors=ignore)
        content = sys.stdin.read()
    else:
        with open(args.input, 'r', encoding=args.from_code,
                  errors=ignore) as f:
            content = f.read()

    if args.output:
        with open(args.output, 'w', encoding=args.to_code) as f:
            f.write(content)
    else:
        sys.stdout.reconfigure(encoding=args.to_code)
        sys.stdout.write(content)


if __name__ == "__main__":
    main()
