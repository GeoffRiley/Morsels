import argparse
from pathlib import Path
from textwrap import dedent
from typing import Dict
from unicodedata import normalize

NATO_ALPHABET = dedent("""A Alfa
                          B Bravo
                          C Charlie
                          D Delta
                          E Echo
                          F Foxtrot
                          G Golf
                          H Hotel
                          I India
                          J Juliett
                          K Kilo
                          L Lima
                          M Mike
                          N November
                          O Oscar
                          P Papa
                          Q Quebec
                          R Romeo
                          S Sierra
                          T Tango
                          U Uniform
                          V Victor
                          W Whiskey
                          X X-ray
                          Y Yankee
                          Z Zulu
                          """)

PHONEMES: Dict[str, str] = {
    k.casefold(): v
    for k, v in (tuple(r.split(maxsplit=2))
                 for r in NATO_ALPHABET.splitlines(keepends=False))
}


def print_word(word: str, notation_file: Path):
    if notation_file:
        phonemes = {
            k.casefold(): v
            for k, v in (tuple(r.split(maxsplit=2))
                         for r in notation_file.read_text().splitlines(
                             keepends=False))
        }
    else:
        phonemes = PHONEMES
    for character in word.casefold():
        if character in phonemes:
            print(phonemes[character])
        elif character.isspace():
            print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('words', nargs='*')
    parser.add_argument('-f',
                        dest='infile',
                        type=Path,
                        nargs='?',
                        default=None)
    args = parser.parse_args()
    word = ' '.join(args.words) if args.words else input('Text to spell out: ')
    print_word(normalize('NFD', word), args.infile)


if __name__ == "__main__":
    main()
