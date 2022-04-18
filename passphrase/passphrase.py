import argparse
import secrets
from math import log2
from pathlib import Path
from sys import stderr
from typing import List


def pick_word(word_list: List[str]):
    return secrets.choice(word_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dictionary', type=Path)
    parser.add_argument('--words', '-w', type=int, default=4)
    parser.add_argument('--verbose', '-v', action='store_true', default=False)

    args = parser.parse_args()

    dictionary = args.dictionary.read_text().splitlines()

    passphrase = ' '.join([pick_word(dictionary) for _ in range(args.words)])
    print(passphrase)

    if args.verbose:
        word_count = len(dictionary)
        entropy = log2(word_count**args.words)
        similar = round(entropy / log2(62))

        print(
            f'This {args.words}-word passphrase picked from {word_count} '
            f'words is similar to a {similar} character password '
            f'(entropy {round(entropy)})',
            file=stderr)


if __name__ == '__main__':
    main()
