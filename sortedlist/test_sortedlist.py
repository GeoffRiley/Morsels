import unittest
from functools import partial
from textwrap import dedent
from timeit import timeit

from sortedlist import SortedList

MANY_BIG_NUMBERS = list(range(10000))


class SortedListTests(unittest.TestCase):
    """Tests for SortedList."""
    def test_sorted_initializer_and_iteration(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(list(numbers), [1, 3, 4, 6, 7, 23, 24])
        self.assertEqual(list(numbers), list(numbers))

    def test_length(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(len(numbers), 7)

    def test_indexing(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(numbers[1], 3)
        self.assertEqual(numbers[-1], 24)

    def test_unordered_setting_and_inserting_not_allowed(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(numbers[1], 3)
        with self.assertRaises(Exception):
            numbers[1] = 8
        with self.assertRaises(Exception):
            numbers.insert(0, 8)
        with self.assertRaises(Exception):
            numbers.append(8)
        self.assertEqual(numbers[0], 1)
        self.assertEqual(numbers[1], 3)
        self.assertEqual(numbers[-1], 24)
        self.assertEqual(len(numbers), 7)

    def test_initializer_copies_input(self):
        input_numbers = [1, 3, 4, 24, 6, 7, 23]
        numbers = SortedList(input_numbers)
        input_numbers.append(100)
        self.assertEqual(list(numbers), [1, 3, 4, 6, 7, 23, 24])
        self.assertEqual(list(numbers), list(numbers))

    def test_string_representation(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(repr(numbers), "SortedList([1, 3, 4, 6, 7, 23, 24])")
        self.assertEqual(str(numbers), repr(numbers))

    def test_sorted_add(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        numbers.add(26)
        self.assertEqual(list(numbers), [1, 3, 4, 6, 7, 23, 24, 26])
        numbers.add(2)
        self.assertEqual(list(numbers), [1, 2, 3, 4, 6, 7, 23, 24, 26])

    def test_sorted_remove(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        numbers.remove(3)
        self.assertEqual(list(numbers), [1, 4, 6, 7, 23, 24])
        with self.assertRaises(ValueError):
            numbers.remove(2)

    def test_index(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(numbers.index(1), 0)
        self.assertEqual(numbers.index(3), 1)
        self.assertEqual(numbers.index(23), 5)
        self.assertEqual(numbers.index(4, stop=3), 2)
        self.assertEqual(numbers.index(4, stop=20), 2)
        self.assertEqual(numbers.index(23, start=4), 5)
        with self.assertRaises(ValueError):
            numbers.index(4, stop=2)
        with self.assertRaises(ValueError):
            numbers.index(23, stop=4)
        with self.assertRaises(ValueError):
            numbers.index(4, start=4)

    def test_containment(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertTrue(1 in numbers)
        self.assertFalse(2 in numbers)
        self.assertTrue(3 in numbers)
        self.assertFalse(5 in numbers)
        self.assertTrue(23 in numbers)
        self.assertTrue(4 in numbers)
        self.assertFalse(21 in numbers)

    def test_sorting_strings(self):
        words = SortedList(['apple', 'lime', 'Lemon'])
        words.add('Banana')
        self.assertEqual(list(words), ['Banana', 'Lemon', 'apple', 'lime'])

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_find_rfind_and_count(self):
        numbers = SortedList([2, 11, 2, 1, 29, 3, 7, 4, 2, 18, 4, 2])
        self.assertEqual(numbers.find(1), 0)
        self.assertEqual(numbers.find(2), 1)
        self.assertEqual(numbers.find(3), 5)
        self.assertEqual(numbers.find(4), 6)
        self.assertEqual(numbers.find(5), -1)
        self.assertEqual(numbers.find(7), 8)
        self.assertEqual(numbers.find(100), -1)
        self.assertEqual(numbers.find(0), -1)

        self.assertEqual(numbers.count(1), 1)
        self.assertEqual(numbers.count(2), 4)
        self.assertEqual(numbers.count(3), 1)
        self.assertEqual(numbers.count(4), 2)
        self.assertEqual(numbers.count(5), 0)
        self.assertEqual(numbers.count(6), 0)
        self.assertEqual(numbers.count(7), 1)

        self.assertEqual(numbers.rfind(1), 0)
        self.assertEqual(numbers.rfind(2), 4)
        self.assertEqual(numbers.rfind(3), 5)
        self.assertEqual(numbers.rfind(4), 7)
        self.assertEqual(numbers.rfind(5), -1)
        self.assertEqual(numbers.rfind(7), 8)
        self.assertEqual(numbers.rfind(100), -1)
        self.assertEqual(numbers.rfind(0), -1)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_time_efficiency(self):
        sorted_list = SortedList(MANY_BIG_NUMBERS)
        unsorted_list = sorted(MANY_BIG_NUMBERS)

        time = partial(timeit, globals=locals(), number=50)

        sorted_add = time(
            dedent("""
            sorted_list.add(0)
            sorted_list.add(4000)
            sorted_list.add(9900)
            sorted_list.add(9999)
        """))
        unsorted_add = time(
            dedent("""
            unsorted_list.insert(unsorted_list.index(0), 0)
            unsorted_list.insert(unsorted_list.index(4000), 4000)
            unsorted_list.insert(unsorted_list.index(9900), 9900)
            unsorted_list.insert(unsorted_list.index(9999), 9999)
        """))
        self.assertLess(sorted_add, unsorted_add)

        sorted_count = time(
            dedent("""
            assert sorted_list.count(1) == 1
            assert sorted_list.count(4500) == 1
            assert sorted_list.count(9900) == 51
            assert sorted_list.count(10000) == 0
        """))
        unsorted_count = time(
            dedent("""
            assert unsorted_list.count(1) == 1
            assert unsorted_list.count(4500) == 1
            assert unsorted_list.count(9900) == 51
            assert unsorted_list.count(10000) == 0
        """))
        self.assertLess(sorted_count, unsorted_count)
        sorted_contains = time(
            dedent("""
            for n in range(-20000, 0, 650):
                assert n not in sorted_list
            for n in range(0, 10000, 650):
                assert n in sorted_list
            for n in range(10000, 20000, 650):
                assert n not in sorted_list
        """))
        unsorted_contains = time(
            dedent("""
            for n in range(-20000, 0, 650):
                assert n not in unsorted_list
            for n in range(0, 10000, 650):
                assert n in unsorted_list
            for n in range(10000, 20000, 650):
                assert n not in unsorted_list
        """))
        self.assertLess(sorted_contains * 1.5, unsorted_contains)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_key_function(self):
        words = SortedList(['apple', 'lime', 'Lemon'], key=str.lower)
        self.assertEqual(list(words), ['apple', 'Lemon', 'lime'])
        words.add('Banana')
        self.assertEqual(list(words), ['apple', 'Banana', 'Lemon', 'lime'])
        self.assertNotIn('banana', words)
        self.assertIn('Banana', words)
        self.assertEqual(words.find('banana'), -1)
        self.assertEqual(words.find('Banana'), 1)
        words.remove('Lemon')
        self.assertEqual(list(words), ['apple', 'Banana', 'lime'])
        words.add('pear')
        self.assertEqual(list(words), ['apple', 'Banana', 'lime', 'pear'])
        self.assertEqual(words.find('LIME'), -1)
        self.assertEqual(words.find('lime'), 2)
        self.assertEqual(words.rfind('LIME'), -1)
        self.assertEqual(words.rfind('lime'), 2)
        self.assertEqual(words.count('LIME'), 0)
        self.assertEqual(words.count('lime'), 1)
        words.add('LIME')
        self.assertEqual(words.count('lime'), 1)
        self.assertEqual(words.count('LIME'), 1)
        words.add('lime')
        self.assertEqual(words.count('lime'), 2)
        self.assertEqual(words.count('LIME'), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
