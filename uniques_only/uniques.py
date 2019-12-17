import collections
import json


def uniques_only(nums: iter):
    pre = set()
    for n in nums:
        if isinstance(n, collections.abc.Hashable):
            p = n
        else:
            p = json.dumps(n)
        if p not in pre:
            pre.add(p)
            yield n
