import unittest

from minmax import minmax


class MinMaxTests(unittest.TestCase):
    """Tests for minmax."""

    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_ordered_numbers(self):
        self.assertIterableEqual(minmax([0, 1, 2, 3, 4]), (0, 4))

    def test_with_out_of_order_numbers(self):
        self.assertIterableEqual(minmax([10, 8, 7, 5.0, 3, 6, 2]), (2, 10))

    def test_single_item(self):
        self.assertIterableEqual(minmax([10]), (10, 10))

    def test_same_item_multiple_times(self):
        self.assertIterableEqual(minmax([8, 8, 8]), (8, 8))
        self.assertIterableEqual(minmax([7, 5, 6, 5, 7]), (5, 7))

    def test_negative_numbers(self):
        self.assertIterableEqual(minmax([-10, -8, -7, -5, -3]), (-10, -3))

    def test_strings(self):
        words = ["alfalfa", "animal", "apple", "acoustic", "axiom"]
        self.assertIterableEqual(minmax(words), ("acoustic", "axiom"))

    def test_mixed_types(self):
        with self.assertRaises(TypeError):
            minmax(['a', 2])

    def test_very_large_numbers(self):
        self.assertIterableEqual(
            minmax([2 ** 1000, -2 ** 1000]),
            (-2 ** 1000, 2 ** 1000),
        )

    def test_error_on_empty_iterable(self):
        with self.assertRaises(ValueError):
            minmax([])

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_key_functions(self):
        words = ["alfalfa", "animal", "apple", "acoustic"]
        self.assertIterableEqual(minmax(words, key=len), ("apple", "acoustic"))

        def a_count(word): return word.count('a')

        self.assertIterableEqual(minmax(words, key=a_count), ("apple", "alfalfa"))
        with self.assertRaises(TypeError):
            minmax([1], lambda x: x)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_with_non_lists(self):
        self.assertIterableEqual(minmax((89, 17, 70, 9)), (9, 89))
        self.assertIterableEqual(minmax({8, 7, 5, 3, 9, 6, 2}), (2, 9))
        self.assertIterableEqual(minmax(n ** 2 for n in range(1, 4)), (1, 9))
        with self.assertRaises(ValueError):
            minmax(iter([]))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_response_min_and_max_attributes(self):
        words = ["alfalfa", "animal", "apple", "acoustic", "axiom"]
        output = minmax(words)
        self.assertIterableEqual(output.min, "acoustic")
        self.assertIterableEqual(output.max, "axiom")


if __name__ == "__main__":
    unittest.main(verbosity=2)
