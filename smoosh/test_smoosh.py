import unittest

from smoosh import *
import smoosh


class SmooshTests(unittest.TestCase):
    """Tests for smoosh."""
    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_already_smooshed(self):
        self.assertIterableEqual(
            smoosh.smoosh([1, 2, 3, 4]),
            [1, 2, 3, 4],
        )

    def test_list_of_lists(self):
        self.assertIterableEqual(
            smoosh.smoosh([[2, 3], [4, 5]]),
            [2, 3, 4, 5],
        )

    def test_mixed_lists_and_non_lists(self):
        self.assertIterableEqual(
            smoosh.smoosh([2, 3, [4, 5]]),
            [2, 3, 4, 5],
        )

    def test_only_smooshes_one_level(self):
        self.assertIterableEqual(
            smoosh.smoosh([1, [2, [3, [4]]]]),
            [1, 2, [3, [4]]],
        )

    def test_non_list_sequences(self):
        self.assertIterableEqual(
            smoosh.smoosh([(1, 2), (3, 4)]),
            [1, 2, 3, 4],
        )
        self.assertIterableEqual(
            smoosh.smoosh([range(5), range(10, 4, -1)]),
            [0, 1, 2, 3, 4, 10, 9, 8, 7, 6, 5],
        )

    def test_strings_are_not_smooshed(self):
        self.assertIterableEqual(
            smoosh.smoosh(['hello', 'these', 'are', 'strings']),
            ['hello', 'these', 'are', 'strings'],
        )

    def test_other_iterables(self):
        self.assertIterableEqual(
            smoosh.smoosh(n**2 for n in range(10)),
            [0, 1, 4, 9, 16, 25, 36, 49, 64, 81],
        )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class SmooooooshTests(unittest.TestCase):
    """Tests for smooosh through smoooooosh."""

    data = [
        2,
        [
            [
                1,
                [
                    3,
                    [
                        4,
                        7,
                        [
                            11,
                            [
                                18,
                                29,
                            ],
                            40,
                            69,
                        ],
                        109,
                    ],
                ],
                178,
            ],
        ],
    ]

    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_smoosh(self):
        self.assertIterableEqual(
            smoosh.smoosh(self.data),
            [2, [1, [3, [4, 7, [11, [18, 29], 40, 69], 109]], 178]],
        )

    def test_smooosh(self):
        self.assertIterableEqual(
            smoosh.smooosh(self.data),
            [2, 1, [3, [4, 7, [11, [18, 29], 40, 69], 109]], 178],
        )

    def test_smoooosh(self):
        self.assertIterableEqual(
            smoosh.smoooosh(self.data),
            [2, 1, 3, [4, 7, [11, [18, 29], 40, 69], 109], 178],
        )

    def test_smooooosh(self):
        self.assertIterableEqual(
            smoosh.smooooosh(self.data),
            [2, 1, 3, 4, 7, [11, [18, 29], 40, 69], 109, 178],
        )

    def test_smoooooosh(self):
        self.assertIterableEqual(
            smoosh.smoooooosh(self.data),
            [2, 1, 3, 4, 7, 11, [18, 29], 40, 69, 109, 178],
        )

    def test_smooooooosh(self):
        self.assertIterableEqual(
            smoosh.smooooooosh(self.data),
            [2, 1, 3, 4, 7, 11, 18, 29, 40, 69, 109, 178],
        )

    def test_strings_are_not_smooshed(self):
        self.assertIterableEqual(
            smoosh.smooooooosh([['hello', ['these', 'are'], 'strings']]),
            ['hello', 'these', 'are', 'strings'],
        )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class VeryDeepSmooshTests(unittest.TestCase):
    """Tests for sm(o*100)sh."""
    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_smooooooooooooooosh(self):
        self.assertIterableEqual(
            smoosh.smooooooooooooooosh([[[[[[[[[[[[[[[['hi']]]]]]]]]]]]]]]]),
            [['hi']],
        )

    def test_100_o_smoosh(self):
        self.assertIterableEqual(
            smoosh.
            smoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooosh(
                range(5)),
            [0, 1, 2, 3, 4],
        )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class SmooshModuleAttributesTests(unittest.TestCase):
    """Tests for from smoosh import *."""

    maxDiff = None

    all_smooshes = {
        'smoosh', 'smooosh', 'smoooosh', 'smooooosh', 'smoooooosh',
        'smooooooosh', 'smoooooooosh', 'smooooooooosh', 'smoooooooooosh'
    }

    def test_star_import(self):
        excluded = {'unittest'}
        self.assertEqual(
            {
                attr
                for attr in globals().keys()
                if '__' not in attr and attr.islower() and attr not in excluded
            },
            self.all_smooshes,
        )

    def test_dir_of_smoosh_module(self):
        self.assertEqual(
            dir(smoosh),
            sorted(self.all_smooshes),
        )


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    import sys
    from platform import python_version
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    del python_version
    del sys
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
