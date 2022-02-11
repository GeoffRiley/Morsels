import argparse
import pathlib
import re
from typing import Dict, Optional


def _part_name_number(ref: str) -> str:
    ref = ref[1:]
    if ref.isdigit():
        return f'N{ref}'
    return ref


def scan(pattern: str, filename: str) -> Optional[Dict[str, str]]:
    parts = re.findall(r'(%.|[^%]*)', pattern)
    if not parts:
        return None
    q = []
    for part in parts:
        if not part:
            continue
        if part.startswith('%'):
            ref = _part_name_number(part)
            part = part[1:]
            if part.isupper():
                q.append(f'(?P<{ref}>[^/]+?)')
            elif part.islower():
                q.append(f'(?P<{ref}>[^/ ]+?)')
            elif part.isdigit():
                q.append(f'(?P<{ref}>[0-9]+)')
            else:
                raise ValueError()
        else:
            q.append(re.escape(part))

    re_query = ''.join(q)

    result = re.match(fr'{re_query}$', filename)

    return result if not result else result.groupdict()


def format(pattern: str, data: Dict[str, str]) -> str:
    parts = re.findall(r'(%.|[^%]*)', pattern)
    if not parts:
        return None
    return ''.join(
        data[_part_name_number(part)] if part and part[0] == '%' else part
        for part in parts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('frompattern')
    parser.add_argument('topattern')

    args = parser.parse_args()

    p = pathlib.Path('.')  # .cwd()
    for file in p.glob('**/*'):
        if file.is_file():
            try:
                fn = str(file)
                if data := scan(args.frompattern, fn):
                    newfile = format(args.topattern, data)
                    print(f'Moving "{fn}" to "{newfile}"')
            except:
                pass
