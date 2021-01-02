from typing import Tuple, Dict


def extract_attributes(code: str) -> Tuple[str, Dict[str, str]]:
    tag = ''
    attrs = {}
    if code[0] != '<' or code[-1] != '>':
        raise ValueError(f'Not a valid HTML tag "{code}"')
    code_parts = code[1:-1].split(' ')
    tag = code_parts.pop(0).lower()
    while code_parts:
        if '=' not in code_parts[0]:
            key = code_parts.pop(0).lower()
            value = 'True'
        else:
            key, value = map(str.lower, code_parts.pop(0).split('=', maxsplit=1))
            while value[0] in '\'"' and value[-1] != value[0]:
                value += f' {code_parts.pop(0).lower()}'
            if value[0] in '\'"':
                value = value[1:-1]
        if key not in attrs:
            attrs[key] = value
    return tag, attrs


def tags_equal(code1: str, code2: str) -> bool:
    t1, a1 = extract_attributes(code1)
    t2, a2 = extract_attributes(code2)
    return t1 == t2 and a1 == a2
