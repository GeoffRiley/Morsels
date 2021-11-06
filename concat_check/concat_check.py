import argparse
from token import NEWLINE, NL, STRING
import tokenize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    for filename in args.files:
        with tokenize.open(filename) as fh:
            tokens = tokenize.generate_tokens(fh.readline)
            last_token = tokenize.TokenInfo(None, None, None, None, None)
            for token in tokens:
                if token.type == last_token.type == STRING:
                    print(f'{filename}, line {last_token.end[0]} between '
                          f'{last_token.string} and {token.string}')
                if token.type not in (NEWLINE, NL):
                    last_token = token


if __name__ == "__main__":
    main()
