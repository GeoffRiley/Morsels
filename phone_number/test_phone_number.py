import unittest

from phone_number import PhoneNumber


class PhoneNumberTests(unittest.TestCase):
    """Tests for PhoneNumber."""
    def test_repr(self):
        number = PhoneNumber("7167762323")
        self.assertEqual(str([number]), "[PhoneNumber('7167762323')]")

    def test_str(self):
        number = PhoneNumber("7167762323")
        self.assertEqual(str(number), "716-776-2323")

    def test_area_code(self):
        number = PhoneNumber("7167762323")
        self.assertEqual(number.area_code, "716")

    def test_prefix(self):
        number = PhoneNumber("7167762323")
        self.assertEqual(number.prefix, "776")

    def test_line_number(self):
        number = PhoneNumber("7167762323")
        self.assertEqual(number.line_number, "2323")

    def test_different_number_formats_accepted(self):
        self.assertEqual(str(PhoneNumber("716-776-2323")), "716-776-2323")
        self.assertEqual(str(PhoneNumber("(212) 664-7665")), "212-664-7665")
        self.assertEqual(str(PhoneNumber("716 - 776 - 2323")), "716-776-2323")
        self.assertEqual(str(PhoneNumber("716 . 776 . 2323")), "716-776-2323")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_non_phone_numbers(self):
        with self.assertRaises(ValueError):
            PhoneNumber("57167762323")
        with self.assertRaises(ValueError):
            PhoneNumber("88-716-776-2323")
        with self.assertRaises(ValueError):
            PhoneNumber("My number is 716-776-2323")
        with self.assertRaises(ValueError):
            PhoneNumber("21 26 64 76 65")
        with self.assertRaises(ValueError):
            PhoneNumber("02126647665")
        with self.assertRaises(ValueError):
            PhoneNumber("212a664b7665")
        with self.assertRaises(ValueError):
            PhoneNumber("2126-647-665")
        self.assertEqual(str(PhoneNumber("716 7762323")), "716-776-2323")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_equality_and_immutability(self):
        n1 = PhoneNumber("716 776 2323")
        n2 = PhoneNumber("(212) 664-7665")
        n3 = PhoneNumber("212-664-7665")
        n4 = PhoneNumber("7167762323")

        # Equality for n1
        self.assertEqual(n1, n1)
        self.assertNotEqual(n1, n2)
        self.assertNotEqual(n1, n3)
        self.assertEqual(n1, n4)
        self.assertEqual(n1 == n2, False)

        # Equality for n2
        self.assertNotEqual(n2, n1)
        self.assertEqual(n2, n2)
        self.assertEqual(n2, n3)
        self.assertNotEqual(n2, n4)
        self.assertEqual(n2 == n2, True)

        # Equality with other objects
        self.assertNotEqual(n1, 4)
        self.assertNotEqual(n1, str(n2))
        self.assertNotEqual(n1, [])

        # Immutability
        with self.assertRaises(Exception):
            n1.area_code = "410"
        with self.assertRaises(Exception):
            n1.prefix = "410"
        with self.assertRaises(Exception):
            n1.line_number = "4105"
        with self.assertRaises(Exception):
            n1.number = "4104104105"
        with self.assertRaises(Exception):
            n1.random_attribute = "4104104105"

        # Hashability
        self.assertEqual(
            {n1, n2, n3, n4},
            {n1, n2},
        )
        self.assertEqual(
            {n1, n2, n3, n4} - {n3},
            {n4},
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_string_formatting(self):
        n1 = PhoneNumber("716 776 2323")
        n2 = PhoneNumber("(212) 664-7665")

        self.assertEqual(f"{n1}", "716-776-2323")
        self.assertEqual(f"{n1:(}", "(716) 776-2323")
        self.assertEqual(f"{n1:-}", "716-776-2323")
        self.assertEqual(f"{n1: }", "716 776 2323")
        self.assertEqual(f"{n1:.}", "716.776.2323")
        self.assertEqual(f"{n1:- }", "716 - 776 - 2323")
        self.assertEqual(f"{n1:. }", "716 . 776 . 2323")
        self.assertEqual(f"{n1:+}", "+17167762323")
        self.assertEqual(f"{n1:+ }", "+1 716 776 2323")

        self.assertEqual(f"{n2:(}", "(212) 664-7665")
        self.assertEqual(f"{n2:-}", "212-664-7665")
        self.assertEqual(f"{n2: }", "212 664 7665")
        self.assertEqual(f"{n2:.}", "212.664.7665")
        self.assertEqual(f"{n2:- }", "212 - 664 - 7665")
        self.assertEqual(f"{n2:. }", "212 . 664 . 7665")
        self.assertEqual(f"{n2:+}", "+12126647665")
        self.assertEqual(f"{n2:+ }", "+1 212 664 7665")


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
