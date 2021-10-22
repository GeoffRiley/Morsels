import unittest
from itertools import count
from loop_tracker import loop_tracker


class LoopTrackerTests(unittest.TestCase):

    """Tests for loop_tracker."""

    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_empty_sequence(self):
        iterator = loop_tracker([])
        self.assertIterableEqual(iterator, [])
        self.assertEqual(len(iterator), 0)

    def test_looping_over_a_list(self):
        iterator = loop_tracker(['red', 'blue', 'green', 'purple'])
        self.assertEqual(len(iterator), 0)
        self.assertEqual(next(iterator), 'red')
        self.assertEqual(len(iterator), 1)
        self.assertIterableEqual(iterator, ['blue', 'green', 'purple'])
        self.assertEqual(len(iterator), 4)

    def test_exhausting_iterator(self):
        iterator = loop_tracker(['red', 'blue', 'green', 'purple'])
        self.assertIterableEqual(iterator, ['red', 'blue', 'green', 'purple'])
        self.assertIterableEqual(iterator, [])
        self.assertEqual(len(iterator), 4)

    def test_with_an_iterator(self):
        iterator = loop_tracker(n**2 for n in range(5, 10))
        self.assertEqual(len(iterator), 0)
        self.assertEqual(next(iterator), 25)
        self.assertEqual(len(iterator), 1)
        self.assertEqual(next(iterator), 36)
        self.assertEqual(len(iterator), 2)
        self.assertEqual(next(iterator), 49)
        self.assertEqual(len(iterator), 3)

    def test_infinitely_long_iterator(self):
        iterator = loop_tracker(count(20))
        self.assertEqual(next(iterator), 20)
        self.assertEqual(next(iterator), 21)
        self.assertEqual(len(iterator), 2)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_empty_accesses(self):
        iterator = loop_tracker((2, 1, 3, 5))
        self.assertEqual(iterator.empty_accesses, 0)
        self.assertEqual(min(iterator), 1)
        self.assertEqual(len(iterator), 4)
        self.assertEqual(iterator.empty_accesses, 1)
        self.assertEqual(tuple(iterator), ())
        self.assertEqual(iterator.empty_accesses, 2)
        self.assertIterableEqual(iterator, [])
        self.assertEqual(iterator.empty_accesses, 3)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_is_empty(self):
        iterator = loop_tracker(iter(['a', 'b']))
        self.assertFalse(iterator.is_empty())
        self.assertEqual(iterator.empty_accesses, 0)
        self.assertEqual(len(iterator), 0)

        self.assertEqual(next(iterator), 'a')
        self.assertFalse(iterator.is_empty())

        self.assertEqual(next(iterator), 'b')
        self.assertTrue(iterator.is_empty())
        self.assertEqual(iterator.empty_accesses, 0)

        self.assertIterableEqual(iterator, [])
        self.assertEqual(iterator.empty_accesses, 1)
        self.assertTrue(iterator.is_empty())
        self.assertEqual(len(iterator), 2)

        with self.assertRaises(StopIteration):
            next(iterator)
        self.assertEqual(iterator.empty_accesses, 2)

        # None values shouldn't mess things up
        iterator = loop_tracker([None])
        self.assertFalse(iterator.is_empty())
        self.assertFalse(iterator.is_empty())
        self.assertEqual(next(iterator), None)
        self.assertTrue(iterator.is_empty())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_first_and_last(self):
        iterator = loop_tracker(n**2 for n in range(5, 10))
        self.assertEqual(len(iterator), 0)
        self.assertFalse(iterator.is_empty())
        self.assertEqual(iterator.first, 25)
        self.assertEqual(iterator.first, 25)
        self.assertEqual(len(iterator), 0)
        with self.assertRaises(AttributeError):
            iterator.last

        self.assertEqual(next(iterator), 25)
        self.assertEqual(iterator.first, 25)
        self.assertEqual(iterator.last, 25)
        self.assertEqual(len(iterator), 1)

        self.assertEqual(next(iterator), 36)
        self.assertEqual(iterator.first, 25)
        self.assertEqual(iterator.last, 36)

        self.assertIterableEqual(iterator, [49, 64, 81])
        self.assertEqual(iterator.first, 25)
        self.assertEqual(iterator.last, 81)

        # None values shouldn't mess things up
        iterator = loop_tracker([None])
        self.assertEqual(iterator.first, None)
        self.assertEqual(next(iterator), None)
        self.assertEqual(iterator.last, None)

        # Empty iterables don't have first or last values
        iterator = loop_tracker([])
        with self.assertRaises(AttributeError):
            self.assertEqual(iterator.first, 0)
        with self.assertRaises(AttributeError):
            self.assertEqual(iterator.last, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)