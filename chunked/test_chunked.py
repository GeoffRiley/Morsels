import unittest

from chunked import chunked


class ChunkInto(unittest.TestCase):
    """Tests for chunked."""

    def assertNestedIterableEqual(self, iterable1, iterable2):
        self.assertEqual(
            [tuple(x) for x in iterable1],
            [tuple(x) for x in iterable2],
        )

    def test_chunking_a_list(self):
        self.assertNestedIterableEqual(
            chunked([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2),
            [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]],
        )

    def test_empty_list(self):
        self.assertNestedIterableEqual(
            chunked([], 3),
            [],
        )

    def test_last_chunk_is_smaller(self):
        self.assertNestedIterableEqual(
            chunked([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 4),
            [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]],
        )

    def test_chunking_other_sequences(self):
        self.assertNestedIterableEqual(
            chunked(('a', 'b', 'c', 'd', 'e', 'f'), 3),
            ['abc', 'def'],
        )
        self.assertNestedIterableEqual(
            chunked('abcdef', 3),
            ['abc', 'def'],
        )
        self.assertNestedIterableEqual(
            chunked(range(100), 50),
            [range(50), range(50, 100)],
        )

    def test_chunk_size_greater_than_length(self):
        self.assertNestedIterableEqual(
            chunked([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 15),
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_chunking_non_sequences(self):
        self.assertNestedIterableEqual(
            chunked((n ** 2 for n in range(10)), 4),
            [(0, 1, 4, 9), (16, 25, 36, 49), (64, 81)],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_iterator_returned(self):
        squares = (n ** 2 for n in range(10))
        output = chunked(squares, 4)
        self.assertEqual(tuple(next(output)), (0, 1, 4, 9))
        self.assertEqual(next(squares), 16)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_fill_value_given(self):
        self.assertNestedIterableEqual(
            chunked((n ** 2 for n in range(10)), 4, fill=0),
            [(0, 1, 4, 9), (16, 25, 36, 49), (64, 81, 0, 0)],
        )
        self.assertNestedIterableEqual(
            chunked((n ** 2 for n in range(10)), 4, fill=None),
            [(0, 1, 4, 9), (16, 25, 36, 49), (64, 81, None, None)],
        )
        with self.assertRaises(TypeError):
            chunked((n ** 2 for n in range(10)), 4, 0)
        self.assertNestedIterableEqual(
            chunked((n ** 2 for n in range(10)), 4, fill=''),
            [(0, 1, 4, 9), (16, 25, 36, 49), (64, 81, '', '')],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
