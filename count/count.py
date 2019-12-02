from collections import Counter


def count_words(text: str) -> dict:
    result = Counter()
    for x in text.split():
        result[x.strip(',.?¿').lower()] += 1
    return dict(result)
