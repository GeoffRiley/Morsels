from collections import Counter
from datetime import date, timedelta
from typing import List, Tuple


def _date_spread(acc: tuple) -> tuple:
    d, *a = acc
    dt = date.fromisoformat(d)

    for diff in (-1, 0, 1):
        yield date.isoformat(dt + timedelta(days=diff)), *a


def _match_trx(needle: List[tuple], haystack: List[tuple]) -> Counter:
    targets = Counter(haystack)
    matched = Counter()

    for t in sorted(needle):
        for dt in _date_spread(t):
            if targets[dt]:
                matched[t] += 1
                targets[dt] -= 1
                break
    return matched


def _add_state(row, found):
    return [*row, 'FOUND' if found else 'MISSING']


def _process_matches(needle: List[tuple], haystack: List[tuple]) -> List[list]:
    matches = _match_trx(needle, haystack)
    match_list = []

    for pin in needle:
        match_list.append(_add_state(pin, found=matches[pin] > 0))
        matches[pin] -= 1
    return match_list


def reconcile_accounts(acc1: List[list],
                       acc2: List[list]) -> Tuple[List[list], List[list]]:
    trx1 = [tuple(r) for r in acc1]
    trx2 = [tuple(r) for r in acc2]

    acc1r = _process_matches(trx1, trx2)
    acc2r = _process_matches(trx2, trx1)

    return acc1r, acc2r
