import unittest

from dicttools import pluck


class PluckTests(unittest.TestCase):

    """Tests for pluck."""

    def test_pluck_top_level(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(pluck(d, 'x'), 40)
        self.assertEqual(pluck(d, 'c'), {'d': 3})

    def test_pluck_one_level_deep(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(pluck(d, 'a.b'), 5)
        self.assertEqual(pluck(d, 'c.d'), 3)

    def test_pluck_many_levels_deep(self):
        d = {'a': {'b': {'c': {'d': {'e': 4}}}}}
        self.assertEqual(pluck(d, 'a.b.c'), {'d': {'e': 4}})
        self.assertEqual(pluck(d, 'a.b.c.d'), {'e': 4})
        self.assertEqual(pluck(d, 'a.b.c.d.e'), 4)

    def test_exception_on_missing_item(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        with self.assertRaises(KeyError):
            pluck(d, 'c.e')
        with self.assertRaises(KeyError):
            pluck(d, 'z')

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_specifying_separator(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(pluck(d, 'c/d', sep='/'), 3)
        self.assertEqual(pluck(d, 'a.b', sep='.'), 5)
        self.assertEqual(pluck(d, 'a z', sep=' '), 20)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_specifying_default_value(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(pluck(d, 'c.e', default=None), None)
        self.assertEqual(pluck(d, 'y.z', default=0), 0)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_multiple_lookups_accepted(self):
        d = {'a': {'b': 5, 'z': 20}, 'c': {'d': 3}, 'x': 40}
        self.assertEqual(
            pluck(d, 'a.b', 'c.e', 'c.d', 'x', default=None),
            (5, None, 3, 40),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)