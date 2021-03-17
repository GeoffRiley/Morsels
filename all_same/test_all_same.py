import unittest

from all_same import all_same


class AllSameTests(unittest.TestCase):

    """Tests for all_same."""

    def test_one_item_number(self):
        self.assertTrue(all_same([4]))
        self.assertTrue(all_same([0]))
        self.assertTrue(all_same([-1]))

    def test_one_string(self):
        self.assertTrue(all_same(['hello']))

    def test_one_none_value(self):
        self.assertTrue(all_same([None]))

    def test_one_tuple(self):
        self.assertTrue(all_same([()]))
        self.assertTrue(all_same([(1,)]))
        self.assertTrue(all_same([(1, 2)]))

    def test_empty_sequence(self):
        self.assertTrue(all_same([]))
        self.assertTrue(all_same(()))
        self.assertTrue(all_same(''))

    def test_two_same_item(self):
        self.assertTrue(all_same([1, 1]))
        self.assertTrue(all_same([0, 0]))
        self.assertTrue(all_same(['hello', 'hello']))
        self.assertTrue(all_same([-1, -1]))
        self.assertTrue(all_same([(1, 2), (1, 2)]))
        self.assertTrue(all_same([None, None]))

    def test_two_different_items(self):
        self.assertFalse(all_same(['hello', 'hi']))
        self.assertFalse(all_same([-1, 1]))
        self.assertFalse(all_same([-1, 'hi']))
        self.assertFalse(all_same([(1, 3), (1, 2)]))
        self.assertFalse(all_same(['hello', (4, 5)]))
        self.assertFalse(all_same([4, None]))
        self.assertFalse(all_same([None, 4]))

    def test_many_items(self):
        self.assertTrue(all_same([1, 1, 1, 1, 1, 1]))
        self.assertFalse(all_same([1, 1, 1, 1, 2, 1]))
        self.assertFalse(all_same(['hi', 'hello', 'hey']))
        self.assertFalse(all_same(['hello', 'hella', 'hello']))
        self.assertTrue(all_same(['hi', 'hi', 'hi', 'hi', 'hi']))
        self.assertTrue(all_same(['hello', 'hello', 'hello']))
        self.assertTrue(all_same([(1, 2, 3), (1, 2, 3), (1, 2, 3)]))
        self.assertFalse(all_same([(1, 2, 3), (1, 2, 3), (1, 4, 3)]))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_nonhashable_values(self):
        self.assertFalse(all_same([['hi', 'hi'], ['hi', 'hi', 'hi']]))
        self.assertTrue(all_same([['hi', 'hi'], ['hi', 'hi']]))
        self.assertTrue(all_same([{1: 2}, {1: 2}]))
        self.assertFalse(all_same([{1: 2}, {1: 3}]))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_nonsequences(self):
        numbers = [1, 3, 5, 7, 9]
        self.assertTrue(all_same({1}))
        self.assertFalse(all_same({1, 2}))
        self.assertFalse(all_same(n**2 for n in numbers))
        self.assertTrue(all_same(n % 2 for n in numbers))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_return_early(self):
        self.assertFalse(all_same(n**2 for n in [2, 3, {}]))
        from itertools import count
        self.assertFalse(all_same(count()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
