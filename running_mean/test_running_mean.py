import unittest

from running_mean import running_mean


class RunningMeanTests(unittest.TestCase):
    """Tests for running_mean."""
    def test_empty_list(self):
        self.assertEqual(list(running_mean([])), [])

    def test_single_item(self):
        self.assertEqual(list(running_mean([10])), [(10, 10)])

    def test_two_items(self):
        self.assertEqual(
            list(running_mean([10, 20])),
            [(10, 10), (20, 15)],
        )

    def test_three_items(self):
        self.assertEqual(
            list(running_mean([10, 15, 20])),
            [(10, 10), (15, 12.5), (20, 15)],
        )

    def test_many_items(self):
        self.assertEqual(
            list(running_mean([3, 8, 4, 7, 18, 11])),
            [(3, 3), (8, 5.5), (4, 5), (7, 5.5), (18, 8), (11, 8.5)],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_output_is_an_iterator(self):
        inputs = iter([3, 8, 4, 7, 18, 11])
        means = running_mean(inputs)
        self.assertEqual(next(means), (3, 3))
        self.assertEqual(next(means), (8, 5.5))
        self.assertEqual(next(inputs), 4)
        self.assertEqual(
            list(means),
            [(7, 6), (18, 9), (11, 9.4)],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_must_have_send_method(self):
        inputs = iter([3, 8, 4, 7, 18, 11])
        means = running_mean(inputs)
        self.assertEqual(next(means), (3, 3))
        self.assertEqual(next(means), (8, 5.5))
        self.assertEqual(next(inputs), 4)
        self.assertEqual(means.send(4), (4, 5))
        self.assertEqual(next(means), (7, 5.5))
        self.assertEqual(next(means), (18, 8))
        self.assertEqual(means.send(14), (14, 9))
        self.assertEqual(means.send(16), (16, 10))
        self.assertEqual(next(means), (11, 10.125))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_flexible_send_and_unexhausting(self):
        inputs = iter([3, 8, 4, 7, 18, 11])
        means = running_mean(inputs)
        self.assertEqual(means.send(4), (4, 4))
        self.assertEqual(next(means), (3, 3.5))
        self.assertEqual(next(means), (8, 5))
        self.assertEqual(means.send(11), (11, 6.5))
        self.assertEqual(next(means), (4, 6))
        x, y, = next(inputs), next(inputs)
        self.assertEqual(means.send(y), (18, 8))
        self.assertEqual(means.send(15), (15, 9))
        self.assertEqual(means.send(x), (7, 8.75))
        self.assertEqual(next(means), (11, 9))
        self.assertEqual(means.send(19), (19, 10))


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
