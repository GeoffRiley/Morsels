from io import StringIO
import unittest

from partial import partial


class PartialTests(unittest.TestCase):
    """Tests for partial."""
    def test_arguments_held_for_later_execution(self):
        def add(x, y):
            return x + y

        add_3_and_4 = partial(add, 3, 4)
        self.assertEqual(add_3_and_4(), 7)
        add_3 = partial(add, 3)
        self.assertEqual(add_3(7), 10)
        add_1_and_4 = partial(add, x=1, y=4)
        self.assertEqual(add_1_and_4(), 5)
        add_4 = partial(add, y=4)
        self.assertEqual(add_4(8), 12)
        self.assertEqual(add_4(8), 12)  # Calling twice works

    def test_with_many_arguments(self):
        template = "{0} {1} and {2} and {red} {green} and {blue}"
        with_four_args = partial(template.format, 1, 2, 3, 4)
        with_kwargs_too = partial(with_four_args, red=4, green=5, blue=6)
        self.assertEqual(with_kwargs_too(), "1 2 and 3 and 4 5 and 6")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_skip_arguments(self):
        from partial import SKIP
        template = "{0} {1} {2} and {3}"
        skip_first = partial(template.format, SKIP, 2)
        skip_last = partial(template.format, 1, 2, SKIP)
        with_two_skips = partial(template.format, SKIP, 2, SKIP)

        # Unevaluated skips
        with self.assertRaises(Exception):
            skip_last()
        with self.assertRaises(Exception):
            skip_last(3)
        with self.assertRaises(Exception):
            with_two_skips(1)
        with self.assertRaises(Exception):
            with_two_skips(1, 2)

        # Correct skips
        self.assertEqual(skip_last(3, 4), "1 2 3 and 4")
        self.assertEqual(with_two_skips(4, 6, 7), "4 2 6 and 7")
        self.assertEqual(with_two_skips(4, 7, 8), "4 2 7 and 8")
        self.assertEqual(skip_first(1, 3, 4), "1 2 3 and 4")

        # Unevaluated skips still don't work
        with self.assertRaises(Exception):
            skip_last()
        with self.assertRaises(Exception):
            skip_last(2)
        with self.assertRaises(Exception):
            with_two_skips(1)
        with self.assertRaises(Exception):
            with_two_skips(3, 4)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_partial_method(self):
        template = "{0} {1} and {2} and {red} {green} and {blue}"
        x = partial(template.format, 'purple', 'white')
        y = x.partial(green=2, blue=3)
        z = y.partial('red', red=1)
        w = y.partial('black', blue=4, green=2)
        self.assertEqual(
            x('pink', green=1, blue=2, red=3),
            "purple white and pink and 3 1 and 2",
            "Original partial shouldn't change on .partial() method call!",
        )
        self.assertEqual(z(), "purple white and red and 1 2 and 3")
        self.assertEqual(w(red=0), "purple white and black and 0 2 and 4")
        self.assertEqual(y(None, red=9), "purple white and None and 9 2 and 3")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_nice_string_representation(self):
        fake_file = StringIO()
        fake_print = partial(print, file=fake_file)
        self.assertIn('print', repr(fake_print))
        self.assertIn('file', repr(fake_print))
        print_one_two_three = fake_print.partial(1, 2, 3)
        self.assertIn('print', repr(print_one_two_three))
        self.assertIn('file', repr(print_one_two_three))
        self.assertIn('1, 2, 3', repr(print_one_two_three))


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    import sys
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
