from contextlib import contextmanager
from datetime import date
from locale import setlocale, LC_TIME
import unittest

from month import Month


class MonthTests(unittest.TestCase):

    """Tests for Month."""

    def test_initializer(self):
        python2_eol = Month(2020, 1)
        self.assertEqual(python2_eol.year, 2020)
        self.assertEqual(python2_eol.month, 1)

    def test_equality(self):
        python2_eol = Month(2020, 1)
        self.assertEqual(python2_eol, Month(2020, 1))
        self.assertNotEqual(python2_eol, Month(2020, 2))
        self.assertNotEqual(python2_eol, Month(2019, 1))
        self.assertFalse(python2_eol != Month(2020, 1))
        self.assertFalse(python2_eol == Month(2020, 2))
        self.assertNotEqual(python2_eol, date(2020, 1, 1))
        self.assertNotEqual(python2_eol, (2020, 1))
        self.assertNotEqual((2020, 1), python2_eol)  # tuples aren't months

    def test_ordering(self):
        python2_eol = Month(2020, 1)
        pycon_2019 = Month(2019, 5)
        self.assertLess(pycon_2019, python2_eol)
        self.assertGreater(python2_eol, pycon_2019)
        self.assertLessEqual(pycon_2019, python2_eol)
        self.assertGreaterEqual(python2_eol, pycon_2019)
        self.assertFalse(pycon_2019 > python2_eol)
        self.assertFalse(pycon_2019 >= python2_eol)
        self.assertFalse(python2_eol < pycon_2019)
        self.assertFalse(python2_eol <= pycon_2019)
        with self.assertRaises(TypeError):
            python2_eol < (2021, 12)  # tuples aren't months
        with self.assertRaises(TypeError):
            python2_eol >= (2021, 12)  # tuples aren't months
        with self.assertRaises(TypeError):
            (2021, 12) < python2_eol  # tuples aren't months

    def test_string_representations(self):
        python2_eol = Month(2020, 1)
        self.assertEqual(str(python2_eol), "2020-01")
        new_month = eval(repr(python2_eol))
        self.assertEqual(new_month.year, python2_eol.year)
        self.assertEqual(new_month.month, python2_eol.month)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_first_day_and_last_day(self):
        python2_eol = Month(2020, 1)
        pycon_2019 = Month(2019, 5)
        leap_month = Month(2000, 2)
        non_leap_month = Month(1900, 2)
        self.assertEqual(python2_eol.first_day, date(2020, 1, 1))
        self.assertEqual(python2_eol.last_day, date(2020, 1, 31))
        self.assertEqual(pycon_2019.first_day, date(2019, 5, 1))
        self.assertEqual(pycon_2019.last_day, date(2019, 5, 31))
        self.assertEqual(leap_month.last_day, date(2000, 2, 29))
        self.assertEqual(non_leap_month.last_day, date(1900, 2, 28))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_from_date_and_strftime(self):
        python2_eol = Month.from_date(date(2020, 1, 1))
        self.assertEqual(python2_eol, Month(2020, 1))
        leap_month = Month.from_date(date(2000, 2, 29))
        self.assertEqual(leap_month, Month(2000, 2))
        self.assertEqual(python2_eol.strftime('%Y-%m'), "2020-01")
        with set_locale('C'):
            self.assertEqual(leap_month.strftime('%b %Y'), "Feb 2000")
            self.assertEqual(python2_eol.strftime('%b %Y'), "Jan 2020")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_immutability(self):
        python2_eol = Month(2020, 1)
        with self.assertRaises(Exception):
            python2_eol.year = 2000
        with self.assertRaises(Exception):
            python2_eol.month = 1
        with self.assertRaises(Exception):
            del python2_eol.year
        with self.assertRaises(Exception):
            del python2_eol.month
        with self.assertRaises(Exception):
            python2_eol.__dict__
        self.assertEqual(hash(python2_eol), hash(Month(2020, 1)))
        self.assertNotEqual(hash(python2_eol), hash(Month(2020, 2)))
        self.assertNotEqual(hash(python2_eol), hash(Month(2019, 1)))
        self.assertNotEqual(hash(python2_eol), hash(Month(2019, 12)))
        self.assertNotEqual(hash(python2_eol), hash(Month(2019, 2)))


@contextmanager
def set_locale(name):
    saved = setlocale(LC_TIME)
    try:
        yield setlocale(LC_TIME, name)
    finally:
        setlocale(LC_TIME, saved)


if __name__ == "__main__":
    unittest.main(verbosity=2)