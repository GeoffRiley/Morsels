"""
Python Morsel Exercise: SortedList

    Make a *SortedList* class. This class will act sort of like a list but the
    items within it will always be in sorted order.

    This list-like structure shouldn't allow *append*, *insert*, or item-
    setting, but should instead have an *add* method to add items in the
    correct sorted position.

    >>> sorted_numbers = SortedList({30, 2, 18, 20, 7, 6})
    >>> sorted_numbers
    SortedList([2, 6, 7, 18, 20, 30])
    >>> sorted_numbers.add(13)
    >>> sorted_numbers
    SortedList([2, 6, 7, 13, 18, 20, 30])

    This *SortedList* class should also have a nice string representation,
    support containment, allow indexing, and have a length. It should have
    *remove* and *index* methods that work the same way as the same methods
    on lists.

    >>> 8 in sorted_numbers
    False
    >>> sorted_numbers.index(6)
    1
    >>> len(sorted_numbers)
    7
    >>> sorted_numbers[-1]
    30
    >>> sorted_numbers.remove(18)
    >>> sorted_numbers
    SortedList([2, 6, 7, 13, 20, 30])

    Note that the *index* method should accept optional *start* and *stop*
    indexes.

    == Bonus 1 ==

    For the first bonus, your *SortedList* class should also have *find*,
    *rfind*, and *count* methods. The *count* method should work the same way
    as on lists and the *find* and *rfind* methods should work similarly to
    the equivalent methods on strings.

    >>> sorted_words = SortedList(['apple', 'lime', 'jujube', 'lime', 'loquat'])
    >>> sorted_words.find('lime')
    2
    >>> sorted_words.rfind('lime')
    3
    >>> sorted_words.find('watermelon')
    -1
    >>> sorted_words.count('lime')
    2
    >>> sorted_words.count('jujube')
    1
    >>> sorted_words.count('watermelon')
    0

    The *find* method will return the first index that a matching item is found
    at and the *rfind* method will return the last index it is found at. Both
    should return *-1* if the item is not in the list.

    == Bonus 2 ==

    For the second bonus, your *SortedList* should be more efficient than a
    regular list for the various operations which require locating elements
    (*add*, *remove*, *count*, *index*, containment, *find*, *rfind*).

    If you're not sure how you might go about accomplishing this talk, check
    the hints for help.

    == Bonus 3 ==

    If you get done with the first two bonuses and you're looking for more of a
    challenge, add an optional *key* argument to your *SortedList* class, which
    will act as the sort key (similar to the *key* argument accepted by
    *sorted*, *min*, and *max*).

    >>> sorted_words = SortedList(['LIME', 'JuJuBe', 'loquat'], key=str.lower)
    >>> sorted_words.add('kiwi')
    >>> sorted_words
    SortedList(['JuJuBe', 'kiwi', 'LIME', 'loquat'])

    == Hints ==

    Hints for when you get stuck (hover over links to see what they're about):

    • Creating a list-like structure in Python (The *collections.abc.
        MutableSequence* class might be useful)
        [https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes]
    • Binary search for sorted lists (Implementing a binary search algorithm in
        Python)
        [https://stackoverflow.com/questions/38346013/binary-search-in-a-python-list]
    • A standard library module that may be helpful (Python's *bisect* module
        includes a number of binary search helpers)
        [https://docs.python.org/3/library/bisect.html]
    • A SortedCollection recipe with a key function (This is pretty much the
        answer)
        [https://code.activestate.com/recipes/577197-sortedcollection/]
    • A much more sophisticated implementation (From the sorted-collections
        module by Grant Jenks)
        [https://github.com/grantjenks/python-sortedcontainers/blob/master/sortedcontainers/sortedlist.py]
    • A 40 minute talk on how that implementation works (No need to watch this
        video unless you're particularly interested in the topic)
        https://pyvideo.org/pycon-us-2016/grant-jenks-python-sorted-collections-pycon-2016.html

"""
from bisect import bisect_left, bisect_right
from typing import Any, Callable, Iterable


class SortedList:
    def __init__(self, values: Iterable = (), *, key: Callable = None) -> None:
        self.provided_key = key
        key = key or (lambda x: x)
        self.used_key = key
        sorted_values = sorted((key(x), x) for x in values)
        self.key_values, self.values = map(list, zip(*sorted_values))

    def __repr__(self) -> str:
        params = ', '.join(str(x) for x in self.values)
        key_s = f', key={self.provided_key!r}' if self.provided_key else ''
        return f'{self.__class__.__name__}([{params}]{key_s})'

    def __iter__(self):
        yield from self.values

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, ndx: int) -> Any:
        return self.values[ndx]

    def add(self, new_item: Any):
        k = self.used_key(new_item)
        i = bisect_left(self.key_values, k)
        self.key_values.insert(i, k)
        self.values.insert(i, new_item)

    def remove(self, old_item: Any):
        if old_item not in self.values:
            raise ValueError
        i = self.index(old_item)
        del self.key_values[i]
        del self.values[i]

    def index(self, value: Any, *, start: int = None, stop: int = None) -> Any:
        start = start or 0
        stop = min(stop or self.__len__(), self.__len__())
        k = self.used_key(value)
        i = bisect_left(self.key_values, k, lo=start, hi=stop)
        if (start <= i < stop) and self.values[i] == value:
            return i
        raise ValueError

    def find(self, value: Any) -> int:
        k = self.used_key(value)
        i = bisect_left(self.key_values, k)
        return i if i < len(self) and self.values[i] == value else -1

    def count(self, value: Any) -> int:
        k = self.used_key(value)
        i = bisect_left(self.key_values, k)
        j = bisect_right(self.key_values, k)
        return self.values[i:j].count(value)

    def rfind(self, value: Any) -> int:
        k = self.used_key(value)
        i = bisect_right(self.key_values, k) - 1
        return i if i < len(self) and self.values[i] == value else -1

    def __contains__(self, value: Any) -> bool:
        k = self.used_key(value)
        i = bisect_left(self.key_values, k)
        j = bisect_right(self.key_values, k)
        return value in self.values[i:j]
