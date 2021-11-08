from contextlib import contextmanager
from io import StringIO
import sys
import unittest


try:
    from prompts import fancy_input, boolean_prompt
except ImportError:
    from prompts import fancy_input


class FancyInputTests(unittest.TestCase):

    """Tests for fancy_input."""

    def test_valid_float(self):
        with patch_stdin('50.5\n'):
            with redirect_output() as out:
                output = fancy_input("Enter your favorite number:", float)
        self.assertEqual(out.getvalue(), "Enter your favorite number: ")
        self.assertEqual(output, 50.5)

    def test_invalid_float_followed_by_valid_float(self):
        with patch_stdin('5j\n  100\n'):
            with redirect_output() as out:
                output = fancy_input("Enter your favorite number:", float)
        self.assertEqual(
            out.getvalue(),
            "Enter your favorite number: "
            "\nPlease enter a valid response.\n\n"
            "Enter your favorite number: "
        )
        self.assertEqual(output, 100.0)

    def test_int_validator(self):
        with patch_stdin('3.0\n5,000\n5000\n'):
            with redirect_output() as out:
                output = fancy_input("Enter your favorite number:", int)
        self.assertEqual(
            out.getvalue(),
            "Enter your favorite number: "
            "\nPlease enter a valid response.\n\n"
            "Enter your favorite number: "
            "\nPlease enter a valid response.\n\n"
            "Enter your favorite number: "
        )
        self.assertEqual(output, 5000)

    def test_raising_other_exception_types(self):
        options = ["blue", "green", "purple"]
        def choice(reply):
            n = int(reply)
            assert n > 0
            return options[n-1]
        with patch_stdin('hi\n5\n-2\n0\n3\n'):
            with redirect_output() as out:
                output = fancy_input("1, 2, or 3?", choice)
        self.assertEqual(
            out.getvalue(),
            "1, 2, or 3? "
            "\nPlease enter a valid response.\n\n"
            "1, 2, or 3? "
            "\nPlease enter a valid response.\n\n"
            "1, 2, or 3? "
            "\nPlease enter a valid response.\n\n"
            "1, 2, or 3? "
            "\nPlease enter a valid response.\n\n"
            "1, 2, or 3? "
        )
        self.assertEqual(output, "purple")

    def test_system_exiting_exceptions_are_not_caught(self):
        def validator(response):
            raise SystemExit
        with patch_stdin('\n\n'):
            with redirect_output():
                with self.assertRaises(SystemExit):
                    fancy_input("Say something:", validator)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_error_message(self):
        def whole_number(string):
            n = int(string)
            if n < 0:
                raise ValueError
            return n
        with patch_stdin('-3\n4.0\n2\n'):
            with redirect_output() as out:
                output = fancy_input(
                    "Enter your favorite number:",
                    whole_number,
                    error_message="Please enter a whole number.")
        self.assertEqual(
            out.getvalue(),
            "Enter your favorite number: "
            "\nPlease enter a whole number.\n\n"
            "Enter your favorite number: "
            "\nPlease enter a whole number.\n\n"
            "Enter your favorite number: "
        )
        self.assertEqual(output, 2)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_writing_to_stderr(self):
        def one_to_a_hundred(string):
            number = int(string)
            assert 1 <= number <= 100
            return number
        with patch_stdin('3.0\n5,000\n50\n'):
            with redirect_output(combine=False) as (out, err):
                output = fancy_input(
                    "Say a number between 1 and 100:",
                    one_to_a_hundred,
                )
        self.assertEqual(output, 50)
        self.assertEqual(
            out.getvalue(),
            "Say a number between 1 and 100: "
            "Say a number between 1 and 100: "
            "Say a number between 1 and 100: "
        )
        self.assertEqual(
            err.getvalue(),
            "\nPlease enter a valid response.\n\n"
            "\nPlease enter a valid response.\n\n"
        )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class BooleanPromptTests(unittest.TestCase):

    """Tests for boolean_prompt."""

    def test_yes(self):
        with patch_stdin('yes\n'):
            with redirect_output() as out:
                output = boolean_prompt("Is the sky blue?")
        self.assertEqual(out.getvalue(), "Is the sky blue? [y/n] ")
        self.assertTrue(output)

    def test_no(self):
        with patch_stdin('no\n'):
            with redirect_output() as out:
                output = boolean_prompt("Yes or no?")
        self.assertEqual(out.getvalue(), "Yes or no? [y/n] ")
        self.assertFalse(output)

    def test_whitespace(self):
        with patch_stdin(' yes  \n'):
            with redirect_output() as out:
                output = boolean_prompt("Is the sky blue?")
        self.assertEqual(out.getvalue(), "Is the sky blue? [y/n] ")
        self.assertTrue(output)

    def test_different_capitalizations(self):
        with patch_stdin('Yes\n'):
            with redirect_output() as out:
                output = boolean_prompt("Yes or no?")
        self.assertEqual(out.getvalue(), "Yes or no? [y/n] ")
        self.assertTrue(output)
        with patch_stdin('NO\n'):
            with redirect_output() as out:
                output = boolean_prompt("Yes or no?")
        self.assertEqual(out.getvalue(), "Yes or no? [y/n] ")
        self.assertFalse(output)

    def test_single_letter_responses(self):
        with patch_stdin('y\n'):
            with redirect_output() as out:
                output = boolean_prompt("Yes or no?")
        self.assertEqual(out.getvalue(), "Yes or no? [y/n] ")
        self.assertTrue(output)
        with patch_stdin('N\n'):
            with redirect_output() as out:
                output = boolean_prompt("Yes or no?")
        self.assertEqual(out.getvalue(), "Yes or no? [y/n] ")
        self.assertFalse(output)

    def test_first_response_invalid(self):
        with patch_stdin('yeah\nyes'):
            with redirect_output(StringIO()) as out:
                output = boolean_prompt("Yes or no?")
        self.assertEqual(
            out.getvalue(),
            "Yes or no? [y/n] "
            "\nPlease enter 'yes' or 'no'.\n\n"
            "Yes or no? [y/n] "
        )
        self.assertTrue(output)

    def test_multiple_invalid_responses(self):
        with patch_stdin('eh\n\nnope\nno'):
            with redirect_output(StringIO()) as out:
                output = boolean_prompt("Yes or no?")
        self.assertEqual(
            out.getvalue(),
            "Yes or no? [y/n] "
            "\nPlease enter 'yes' or 'no'.\n\n"
            "Yes or no? [y/n] "
            "\nPlease enter 'yes' or 'no'.\n\n"
            "Yes or no? [y/n] "
            "\nPlease enter 'yes' or 'no'.\n\n"
            "Yes or no? [y/n] "
        )
        self.assertFalse(output)

    def test_default_of_true(self):
        with patch_stdin('\n'):
            with redirect_output(StringIO()) as out:
                output = boolean_prompt("Yes or no?", default=True)
        self.assertEqual(out.getvalue(), "Yes or no? [Y/n] ")
        self.assertTrue(output)

    def test_default_of_false(self):
        with patch_stdin('\n'):
            with redirect_output(StringIO()) as out:
                output = boolean_prompt("Yes or no?", default=False)
        self.assertEqual(out.getvalue(), "Yes or no? [y/N] ")
        self.assertFalse(output)

    def test_default_with_nonblank_responses(self):
        with patch_stdin('yep\nyes\n'):
            with redirect_output(StringIO()) as out:
                output = boolean_prompt("Yes or no?", default=True)
        self.assertEqual(
            out.getvalue(),
            "Yes or no? [Y/n] "
            "\nPlease enter 'yes' or 'no'.\n\n"
            "Yes or no? [Y/n] "
        )
        self.assertTrue(output)

    def test_default_with_valid_response(self):
        with patch_stdin('nope\nNo\n'):
            with redirect_output(StringIO()) as out:
                output = boolean_prompt("Yes or no?", default=True)
        self.assertEqual(
            out.getvalue(),
            "Yes or no? [Y/n] "
            "\nPlease enter 'yes' or 'no'.\n\n"
            "Yes or no? [Y/n] "
        )
        self.assertFalse(output)
        with patch_stdin('YES\n'):
            with redirect_output(StringIO()) as out:
                output = boolean_prompt("Yes or no?", default=True)
        self.assertEqual(out.getvalue(), "Yes or no? [Y/n] ")
        self.assertTrue(output)


@contextmanager
def patch_stdin(text):
    real_stdin = sys.stdin
    sys.stdin = StringIO(text)
    try:
        yield sys.stdin
    except EOFError as e:
        raise AssertionError("Kept prompting for input too long") from e
    finally:
        sys.stdin = real_stdin


@contextmanager
def redirect_output(combine=True):
    real_stdout, real_stderr = sys.stdout, sys.stderr
    sys.stdout = StringIO()
    sys.stderr = sys.stdout if combine else StringIO()
    try:
        if combine:
            yield sys.stdout
        else:
            yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = real_stdout, real_stderr


if __name__ == "__main__":
    unittest.main(verbosity=2)