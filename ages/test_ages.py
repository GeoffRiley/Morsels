from contextlib import contextmanager
from fractions import Fraction
import unittest


class IsOverTests(unittest.TestCase):

    """Tests for is_over."""

    def test_over_65(self):
        with set_date(2000, 3, 16):
            self.assertTrue(is_over(65, '1935-01-08'))
            self.assertFalse(is_over(65, '1935-04-08'))

    def test_over_18(self):
        with set_date(2000, 2, 1):
            self.assertTrue(is_over(18, '1980-05-20'))
            self.assertTrue(is_over(18, '1980-01-20'))
            self.assertFalse(is_over(18, '1990-12-31'))
            self.assertTrue(is_over(18, '1982-01-31'))
            self.assertTrue(is_over(18, '1982-02-01'))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_leap_days(self):
        """Test with a leap day birthday."""
        with set_date(2018, 3, 16):
            self.assertTrue(is_over(41, '1976-02-29'))
            self.assertTrue(is_over(42, '1976-02-29'))
            self.assertFalse(is_over(43, '1976-02-29'))
        with set_date(2016, 2, 29):
            self.assertTrue(is_over(40, '1976-02-28'))
            self.assertTrue(is_over(1, '2015-02-28'))
            self.assertFalse(is_over(1, '2015-03-01'))
            self.assertTrue(is_over(201, '1815-02-28'))
            self.assertFalse(is_over(201, '1815-03-01'))
            self.assertTrue(is_over(1001, '1015-02-28'))
            self.assertFalse(is_over(1002, '1015-02-28'))


# @unittest.expectedFailure
class GetAgeTests(unittest.TestCase):

    """Tests for get_age."""

    def test_simple_age(self):
        """Test without requiring it work with leap years."""
        with set_date(2017, 3, 16):
            self.assertEqual(get_age('1942-01-08'), 75)

    def test_born_yesterday(self):
        """Test if the birthdate is yesterday."""
        with set_date(2017, 3, 16):
            self.assertEqual(get_age('2017-03-15'), 0)

    def test_years_old(self):
        """Test for ten years ago."""
        with set_date(2017, 3, 16):
            self.assertEqual(get_age('2007-03-16'), 10)

    def test_ten_years_old_tomorrow(self):
        """Test if ten years old tomorrow."""
        with set_date(2015, 7, 4):
            self.assertEqual(get_age('2005-07-05'), 9)

    def test_ten_years_old_yesterday(self):
        """Test if ten years old yesterday."""
        with set_date(2015, 7, 4):
            self.assertEqual(get_age('2005-07-03'), 10)

    def test_leap_days(self):
        """Test with a leap day birthday."""
        with set_date(2018, 3, 16):
            self.assertEqual(get_age('1976-02-29'), 42)
        with set_date(2016, 2, 29):
            self.assertEqual(get_age('1976-02-28'), 40)
            self.assertEqual(get_age('2015-02-28'), 1)
            self.assertEqual(get_age('2015-03-01'), 0)
            self.assertEqual(get_age('1815-02-28'), 201)
            self.assertEqual(get_age('1815-03-01'), 200)
            self.assertEqual(get_age('1015-02-28'), 1001)


# @unittest.expectedFailure
class MoreGetAgeTests(unittest.TestCase):

    def test_exact_age(self):
        """Test for exact age."""
        with set_date(2018, 3, 17):
            birthdate = '1979-12-25'
            age = 38 + Fraction('82/365')
            self.assertEqual(get_age(birthdate, exact=True), age)
        with set_date(2016, 3, 17):
            birthdate = '1979-12-25'
            age = 36 + Fraction('83/366')
            self.assertAlmostEqual(get_age(birthdate, exact=True), age)


def is_over(*args, **kwargs):
    """Call a fresh import of the ages.is_over function."""
    from importlib import reload
    import ages
    reload(ages)
    return ages.is_over(*args, **kwargs)


def get_age(*args, **kwargs):
    """Call a fresh import of the ages.get_age function."""
    from importlib import reload
    import ages
    reload(ages)
    return ages.get_age(*args, **kwargs)


@contextmanager
def set_date(year, month, day):
    """Monkey patch the current time to be the given time."""
    import datetime
    from unittest.mock import patch

    class FakeDate(datetime.date):
        """A datetime.date class with mocked today method."""

        @classmethod
        def today(cls):
            return cls(year, month, day)

    class FakeDateTime(datetime.datetime):
        """A datetime.datetime class with mocked today, now methods."""

        @classmethod
        def today(cls):
            return cls(year, month, day)

        @classmethod
        def now(cls):
            return cls.today()

    with patch('datetime.datetime', FakeDateTime):
        with patch('datetime.date', FakeDate):
            yield


if __name__ == "__main__":
    unittest.main(verbosity=2)
