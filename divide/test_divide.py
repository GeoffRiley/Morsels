import unittest

from divide import divide


class DivideTests(unittest.TestCase):

    """Tests for divide."""

    def assertNestedIterableEqual(self, iterable1, iterable2):
        self.assertEqual(
            [tuple(x) for x in iterable1],
            [tuple(x) for x in iterable2],
        )

    def test_dividing_a_list_into_two(self):
        self.assertNestedIterableEqual(
            divide([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2),
            [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]],
        )

    def test_dividing_string_sequences(self):
        self.assertNestedIterableEqual(
            divide('abcdef', 2),
            [('a', 'b', 'c'), ('d', 'e', 'f')],
        )

    def test_empty_sequence(self):
        self.assertNestedIterableEqual(
            divide([], 2),
            [[], []],
        )

    def test_n_longer_than_length(self):
        self.assertNestedIterableEqual(
            divide([1, 2, 3], 5),
            [[1], [2], [3], [], []],
        )

    def test_dividing_a_list_into_three(self):
        self.assertNestedIterableEqual(
            divide([0, 1, 2, 3, 4, 5, 6, 7, 8], 3),
            [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        )

    def test_dividing_range(self):
        self.assertNestedIterableEqual(
            divide(range(5), 2),
            [range(0, 3), range(3, 5)],
        )

    def test_uneven_parts(self):
        self.assertNestedIterableEqual(
            divide(range(10), 3),
            [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]
        )
        self.assertNestedIterableEqual(
            divide(range(10), 4),
            [[0, 1, 2], [3, 4, 5], [6, 7], [8, 9]]
        )
        self.assertNestedIterableEqual(
            divide(range(8), 5),
            [[0, 1], [2, 3], [4, 5], [6], [7]]
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_iterator_returned(self):
        output = divide(range(10), 4)
        self.assertEqual(list(next(output)), [0, 1, 2])
        self.assertEqual(list(next(output)), [3, 4, 5])
        self.assertEqual(list(next(output)), [6, 7])
        self.assertEqual(list(next(output)), [8, 9])

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_partial_length_for_sequence(self):
        squares = (n**2 for n in range(10))
        self.assertNestedIterableEqual(
            divide(squares, 4, length=10),
            [[0, 1, 4], [9, 16, 25], [36, 49], [64, 81]],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_fill_value(self):
        self.assertNestedIterableEqual(
            divide(range(4), 6, fill='*'),
            [[0], [1], [2], [3], ['*'], ['*']],
        )
        with self.assertRaises(TypeError):
            divide(range(4), 6, '*')
        self.assertNestedIterableEqual(
            divide(range(10), n=4, fill=0),
            [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 0, 0]],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)