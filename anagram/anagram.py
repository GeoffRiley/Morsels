from collections import Counter
from string import punctuation

from unicodedata import normalize


def is_anagram(string1: str, string2: str) -> bool:
    test1 = process_string(string1)
    test2 = process_string(string2)
    return test1 == test2


def process_string(string: str) -> Counter:
    string = normalize('NFKD', ''.join([c.lower()
                                        for c in string
                                        if c not in ' ' + punctuation]
                                       )).encode('ascii',
                                                 'ignore')
    return Counter(string)
