import unittest

from minmax2 import minmax


class MinMaxTests(unittest.TestCase):

    """Tests for minmax."""

    def test_ordered_numbers(self):
        self.assertEqual(minmax([0, 1, 2, 3, 4]), (0, 4))

    def test_with_out_of_order_numbers(self):
        self.assertEqual(minmax([10, 8, 7, 5.0, 3, 6, 2]), (2, 10))

    def test_single_item(self):
        self.assertEqual(minmax([10]), (10, 10))

    def test_same_item_multiple_times(self):
        self.assertEqual(minmax([8, 8, 8]), (8, 8))
        self.assertEqual(minmax([7, 5, 6, 5, 7]), (5, 7))

    def test_negative_numbers(self):
        self.assertEqual(minmax([-10, -8, -7, -5, -3]), (-10, -3))

    def test_strings(self):
        words = ["alfalfa", "animal", "apple", "acoustic", "axiom"]
        self.assertEqual(minmax(words), ("acoustic", "axiom"))

    def test_mixed_types(self):
        with self.assertRaises(TypeError):
            minmax(['a', 2])

    def test_very_large_numbers(self):
        self.assertEqual(minmax([2**1000, -2**1000]), (-2**1000, 2**1000))

    def test_error_on_empty_iterable(self):
        with self.assertRaises(ValueError):
            minmax([])

    def test_default_value(self):
        self.assertEqual(minmax([], default=0), (0, 0))
        self.assertEqual(minmax([], default=None), (None, None))
        self.assertEqual(minmax([], default='a'), ('a', 'a'))
        self.assertEqual(minmax([-10], default='a'), (-10, -10))
        self.assertEqual(minmax([10], default='a'), (10, 10))
        with self.assertRaises(TypeError):
            minmax([1], 0)

    def test_key_functions(self):
        words = ["alfalfa", "animal", "apple", "acoustic"]
        self.assertEqual(minmax(words, key=len), ("apple", "acoustic"))
        def a_count(word): return word.count('a')
        self.assertEqual(minmax(words, key=a_count), ("apple", "alfalfa"))
        with self.assertRaises(TypeError):
            minmax([1], lambda x: x)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_with_non_lists(self):
        self.assertEqual(minmax((89, 17, 70, 9)), (9, 89))
        self.assertEqual(minmax({8, 7, 5, 3, 9, 6, 2}), (2, 9))
        self.assertEqual(minmax(n**2 for n in range(1, 4)), (1, 9))
        with self.assertRaises(ValueError):
            minmax(iter([]))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_response_min_and_max_attributes(self):
        words = ["alfalfa", "animal", "apple", "acoustic", "axiom"]
        output = minmax(words)
        self.assertEqual(output.min, "acoustic")
        self.assertEqual(output.max, "axiom")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_any_number_of_arguments(self):
        self.assertEqual(minmax(1, 8, 3, 9, 2), (1, 9))
        self.assertEqual(minmax('hi', 'hey'), ('hey', 'hi'))
        self.assertEqual(minmax('a'), ('a', 'a'))
        self.assertEqual(minmax('abcd'), ('a', 'd'))
        with self.assertRaises(TypeError):
            minmax()


if __name__ == "__main__":
    unittest.main(verbosity=2)
