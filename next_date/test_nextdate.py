from contextlib import contextmanager
from datetime import date
import unittest

from nextdate import Weekday


class NextDateTests(unittest.TestCase):
    """Tests for NextDate."""
    def setUp(self):
        self.patched_date = patch_date(2019, 9, 3, 10, 30)
        self.set_date = self.patched_date.__enter__()

    def tearDown(self):
        self.patched_date.__exit__(None, None, None)

    def test_date_for_changing_time(self):
        monday = NextDate(Weekday.MONDAY)
        tuesday = NextDate(Weekday.TUESDAY)
        wednesday = NextDate(Weekday.WEDNESDAY)
        thursday = NextDate(Weekday.THURSDAY)
        friday = NextDate(Weekday.FRIDAY)
        saturday = NextDate(Weekday.SATURDAY)
        sunday = NextDate(Weekday.SUNDAY)
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(monday.date(), date(2019, 9, 9))
        self.assertEqual(tuesday.date(), date(2019, 9, 3))
        self.assertEqual(wednesday.date(), date(2019, 9, 4))
        self.assertEqual(thursday.date(), date(2019, 9, 5))
        self.assertEqual(friday.date(), date(2019, 9, 6))
        self.assertEqual(saturday.date(), date(2019, 9, 7))
        self.assertEqual(sunday.date(), date(2019, 9, 8))
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(monday.date(), date(2019, 9, 9))
        self.assertEqual(tuesday.date(), date(2019, 9, 10))
        self.assertEqual(wednesday.date(), date(2019, 9, 11))
        self.assertEqual(thursday.date(), date(2019, 9, 5))
        self.assertEqual(friday.date(), date(2019, 9, 6))
        self.assertEqual(saturday.date(), date(2019, 9, 7))
        self.assertEqual(sunday.date(), date(2019, 9, 8))

    def test_days_until(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(NextDate(Weekday.MONDAY).days_until(), 6)
        self.assertEqual(NextDate(Weekday.TUESDAY).days_until(), 0)
        self.assertEqual(NextDate(Weekday.WEDNESDAY).days_until(), 1)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_nice_string_representation(self):
        self.set_date(2019, 9, 3)  # Tuesday
        monday = NextDate(Weekday.MONDAY)
        monday2 = NextDate(Weekday.MONDAY)
        tuesday = (NextDate(Weekday.TUESDAY))
        self.assertEqual(repr(monday), repr(monday2))
        self.assertNotEqual(repr(monday), repr(tuesday))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_after_today(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(NextDate(Weekday.TUESDAY).days_until(), 0)
        self.assertEqual(
            NextDate(Weekday.TUESDAY, after_today=True).days_until(),
            7,
        )
        self.assertEqual(NextDate(Weekday.WEDNESDAY).days_until(), 1)
        self.assertNotEqual(
            NextDate(Weekday.MONDAY),
            NextDate(Weekday.MONDAY, after_today=True),
        )
        self.assertNotEqual(
            repr(NextDate(Weekday.MONDAY)),
            repr(NextDate(Weekday.MONDAY, after_today=True)),
            "after_today should show up in the string representation",
        )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class FunctionTests(unittest.TestCase):
    """Tests for next_date and days_until."""
    def setUp(self):
        self.patched_date = patch_date(2019, 9, 3, 10, 30)
        self.set_date = self.patched_date.__enter__()

    def tearDown(self):
        self.patched_date.__exit__(None, None, None)

    def test_next_date(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(next_date(Weekday.MONDAY), date(2019, 9, 9))
        self.assertEqual(next_date(Weekday.TUESDAY), date(2019, 9, 3))
        self.assertEqual(next_date(Weekday.WEDNESDAY), date(2019, 9, 4))
        self.assertEqual(next_date(Weekday.THURSDAY), date(2019, 9, 5))
        self.assertEqual(next_date(Weekday.FRIDAY), date(2019, 9, 6))
        self.assertEqual(next_date(Weekday.SATURDAY), date(2019, 9, 7))
        self.assertEqual(next_date(Weekday.SUNDAY), date(2019, 9, 8))
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(next_date(Weekday.MONDAY), date(2019, 9, 9))
        self.assertEqual(next_date(Weekday.TUESDAY), date(2019, 9, 10))
        self.assertEqual(next_date(Weekday.WEDNESDAY), date(2019, 9, 11))
        self.assertEqual(next_date(Weekday.THURSDAY), date(2019, 9, 5))
        self.assertEqual(next_date(Weekday.FRIDAY), date(2019, 9, 6))
        self.assertEqual(next_date(Weekday.SATURDAY), date(2019, 9, 7))
        self.assertEqual(next_date(Weekday.SUNDAY), date(2019, 9, 8))

    def test_days_until(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(days_until(Weekday.MONDAY), 6)
        self.assertEqual(days_until(Weekday.TUESDAY), 0)
        self.assertEqual(days_until(Weekday.WEDNESDAY), 1)
        self.assertEqual(days_until(Weekday.THURSDAY), 2)
        self.assertEqual(days_until(Weekday.FRIDAY), 3)
        self.assertEqual(days_until(Weekday.SATURDAY), 4)
        self.assertEqual(days_until(Weekday.SUNDAY), 5)
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(days_until(Weekday.MONDAY), 4)
        self.assertEqual(days_until(Weekday.TUESDAY), 5)
        self.assertEqual(days_until(Weekday.WEDNESDAY), 6)
        self.assertEqual(days_until(Weekday.THURSDAY), 0)
        self.assertEqual(days_until(Weekday.FRIDAY), 1)
        self.assertEqual(days_until(Weekday.SATURDAY), 2)
        self.assertEqual(days_until(Weekday.SUNDAY), 3)

    def test_days_to_tuesday(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(days_to_tuesday(), 0)
        self.assertEqual(days_to_tuesday(after_today=True), 7)
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(days_to_tuesday(), 5)
        self.assertEqual(days_to_tuesday(after_today=True), 5)

    def test_next_tuesday(self):
        self.set_date(2019, 9, 3)  # Tuesday
        self.assertEqual(next_tuesday(), date(2019, 9, 3))
        self.assertEqual(next_tuesday(after_today=True), date(2019, 9, 10))
        self.set_date(2019, 9, 5)  # Thursday
        self.assertEqual(next_tuesday(), date(2019, 9, 10))
        self.assertEqual(next_tuesday(after_today=True), date(2019, 9, 10))


def NextDate(*args, **kwargs):
    """Call a fresh import of the nextdate.NextDate class."""
    from importlib import reload
    import nextdate
    reload(nextdate)
    return nextdate.NextDate(*args, **kwargs)


def next_date(*args, **kwargs):
    """Call a fresh import of the nextdate.next_date function."""
    from importlib import reload
    import nextdate
    reload(nextdate)
    return nextdate.next_date(*args, **kwargs)


def days_until(*args, **kwargs):
    """Call a fresh import of the nextdate.days_until function."""
    from importlib import reload
    import nextdate
    reload(nextdate)
    return nextdate.days_until(*args, **kwargs)


def days_to_tuesday(*args, **kwargs):
    """Call a fresh import of the nextdate.days_to_tuesday function."""
    from importlib import reload
    import nextdate
    reload(nextdate)
    return nextdate.days_to_tuesday(*args, **kwargs)


def next_tuesday(*args, **kwargs):
    """Call a fresh import of the nextdate.next_tuesday function."""
    from importlib import reload
    import nextdate
    reload(nextdate)
    return nextdate.next_tuesday(*args, **kwargs)


@contextmanager
def patch_date(year, month, day, hour=0, minute=0):
    """Monkey patch the current time to be the given time."""
    import datetime
    from unittest.mock import patch

    date_args = year, month, day
    time_args = hour, minute

    class FakeDate(datetime.date):
        """A datetime.date class with mocked today method."""
        @classmethod
        def today(cls):
            return cls(*date_args)

    class FakeDateTime(datetime.datetime):
        """A datetime.datetime class with mocked today, now methods."""
        @classmethod
        def today(cls):
            return cls(*date_args, *time_args)

        @classmethod
        def now(cls):
            return cls.today()

        @classmethod
        def utcnow(cls):
            return cls.now()

    def set_date(year, month, day, *rest):
        nonlocal date_args, time_args
        date_args = year, month, day
        time_args = rest

    with patch('datetime.datetime', FakeDateTime):
        with patch('datetime.date', FakeDate):
            yield set_date


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
