import re
import argparse


def semantic_wrap(text: str) -> str:
    res = text.replace('\n', '¤NL¤')
    res = re.sub(r"([.!?][\"']?)\s+", r"\1\n", res)
    return res.replace('¤NL¤', '\n')


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('infile')
    args = parse.parse_args()

    with open(args.infile, "r", encoding="UTF-8") as f:
        text = f.read()
        print(semantic_wrap(text), end='')


if __name__ == '__main__':
    main()
