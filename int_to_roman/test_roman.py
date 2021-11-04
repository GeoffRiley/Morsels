import unittest

from roman import int_to_roman


class IntToRomanTests(unittest.TestCase):

    """Tests for int_to_roman."""

    def verify(self, integer, numeral):
        self.assertEqual(int_to_roman(integer), numeral)

    def test_single_digit(self):
        self.verify(1, "I")
        self.verify(5, "V")
        self.verify(10, "X")
        self.verify(50, "L")
        self.verify(100, "C")
        self.verify(500, "D")
        self.verify(1000, "M")

    def test_two_digits_ascending(self):
        self.verify(2, "II")
        self.verify(6, "VI")
        self.verify(11, "XI")
        self.verify(15, "XV")
        self.verify(20, "XX")
        self.verify(60, "LX")
        self.verify(101, "CI")
        self.verify(105, "CV")
        self.verify(110, "CX")
        self.verify(150, "CL")
        self.verify(550, "DL")
        self.verify(600, "DC")
        self.verify(1100, "MC")
        self.verify(2000, "MM")

    def test_three_digits_ascending(self):
        self.verify(3, "III")
        self.verify(7, "VII")
        self.verify(12, "XII")
        self.verify(16, "XVI")
        self.verify(21, "XXI")
        self.verify(25, "XXV")
        self.verify(30, "XXX")

    def test_four_digits_ascending(self):
        self.verify(8, "VIII")
        self.verify(13, "XIII")
        self.verify(17, "XVII")
        self.verify(22, "XXII")
        self.verify(26, "XXVI")
        self.verify(31, "XXXI")
        self.verify(35, "XXXV")

    def test_many_digits(self):
        self.verify(1888, "MDCCCLXXXVIII")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_subtractive(self):
        self.verify(4, "IV")
        self.verify(9, "IX")
        self.verify(14, "XIV")
        self.verify(19, "XIX")
        self.verify(24, "XXIV")
        self.verify(29, "XXIX")
        self.verify(40, "XL")
        self.verify(90, "XC")
        self.verify(44, "XLIV")
        self.verify(94, "XCIV")
        self.verify(49, "XLIX")
        self.verify(99, "XCIX")
        self.verify(1999, "MCMXCIX")
        self.verify(1948, "MCMXLVIII")


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class RomanToIntTests(unittest.TestCase):

    """Tests for roman_to_int."""

    def verify(self, numeral, integer):
        from roman import roman_to_int
        self.assertEqual(roman_to_int(numeral), integer)

    def test_single_digit(self):
        self.verify("I", 1)
        self.verify("V", 5)
        self.verify("X", 10)

    def test_two_digits_ascending(self):
        self.verify("II", 2)
        self.verify("VI", 6)
        self.verify("XI", 11)
        self.verify("XV", 15)
        self.verify("XX", 20)

    def test_three_digits_ascending(self):
        self.verify("III", 3)
        self.verify("VII", 7)
        self.verify("XII", 12)
        self.verify("XVI", 16)
        self.verify("XXI", 21)
        self.verify("XXV", 25)
        self.verify("XXX", 30)

    def test_four_digits_ascending(self):
        self.verify("VIII", 8)
        self.verify("XIII", 13)
        self.verify("XVII", 17)
        self.verify("XXII", 22)
        self.verify("XXVI", 26)
        self.verify("XXXI", 31)
        self.verify("XXXV", 35)

    def test_invalid_numeral(self):
        from roman import roman_to_int
        with self.assertRaises(ValueError):
            roman_to_int("CAT")


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class MoreRomanToIntTests(unittest.TestCase):

    def verify(self, numeral, integer):
        from roman import roman_to_int
        self.assertEqual(roman_to_int(numeral), integer)

    def test_subtractive(self):
        self.verify("IV", 4)
        self.verify("IX", 9)
        self.verify("XIV", 14)
        self.verify("XIX", 19)
        self.verify("XXIV", 24)
        self.verify("XXIX", 29)
        self.verify("MCMXLVIII", 1948)


if __name__ == "__main__":
    unittest.main(verbosity=2)
