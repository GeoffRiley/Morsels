from contextlib import contextmanager, redirect_stdout
import gc
from io import StringIO
from importlib.machinery import SourceFileLoader
import os
import sys
from textwrap import dedent
from tempfile import NamedTemporaryFile
import unittest
import warnings


class UnsmartTests(unittest.TestCase):

    """Tests for unsmart"""

    def assert_expected_output(self, file_contents, expected_output):
        with make_file(file_contents) as filename:
            output = run_program('unsmart.py', [filename])
        self.assertEqual(output.splitlines(), expected_output.splitlines())

    def test_with_smart_quotes(self):
        contents = '“This is a quotation”'
        expected = '"This is a quotation"'
        self.assert_expected_output(contents, expected)

    def test_with_smart_single_quotes(self):
        contents = "This word is ‘quoted’."
        expected = "This word is 'quoted'."
        self.assert_expected_output(contents, expected)

    def test_with_smart_apostrophe(self):
        contents = "Look, it’s an apostrophe!"
        expected = "Look, it's an apostrophe!"
        self.assert_expected_output(contents, expected)

    def test_multiple_lines(self):
        contents = dedent("""
            This text has a number of “smart quotes”. For example there’s a “quotation with ‘nested’ quotes”.

            There’s also a second paragraph. It has a bit of text in it. But its’ text isn’t very meaningful. ‘Tis just an example of text with smart quotes.
        """).lstrip()
        expected = dedent("""
            This text has a number of "smart quotes". For example there's a "quotation with 'nested' quotes".

            There's also a second paragraph. It has a bit of text in it. But its' text isn't very meaningful. 'Tis just an example of text with smart quotes.
        """).lstrip()
        self.assert_expected_output(contents, expected)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_dashes_and_apostrophes(self):
        contents = dedent("""
            We have some dashed–text here — with both en dashes and em dashes.

            There’s also a bit of … ellipsated text…. That’s a word which is totally sensible to use when discussing ellipses.
        """).lstrip()
        expected = dedent("""
            We have some dashed-text here -- with both en dashes and em dashes.

            There's also a bit of ... ellipsated text.... That's a word which is totally sensible to use when discussing ellipses.
        """).lstrip()
        self.assert_expected_output(contents, expected)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_strip_whitespace(self):
        contents = (
            "Whitespace  \nshould be stripped \n \n\n\n"
            "From the ends of lines    \n  But not from the beginning \n"
        )
        expected = (
            "Whitespace\nshould be stripped\n\n\n\n"
            "From the ends of lines\n  But not from the beginning\n"
        )
        self.assert_expected_output(contents, expected)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_standard_input_accepted_with_dash(self):
        contents = dedent("""
            This text has:
            - “double quotes”
            - ‘single quotes’
            - … ellipsis
            - em—dashes
            - en – dashes
            - text
        """).lstrip()
        expected = dedent("""
            This text has:
            - "double quotes"
            - 'single quotes'
            - ... ellipsis
            - em--dashes
            - en - dashes
            - text
        """).lstrip()
        with patch_stdin(contents):
            output = run_program('unsmart.py', ['-'])
        self.assertEqual(output.splitlines(), expected.splitlines())


class DummyException(Exception):
    """No code will ever raise this exception."""


@contextmanager
def patch_stdin(contents):
    old_stdin = sys.stdin
    sys.stdin = StringIO(contents)
    try:
        yield
    finally:
        sys.stdin = old_stdin


def run_program(path, args=[], raises=DummyException):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.
    """
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    warnings.simplefilter("ignore", ResourceWarning)
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            try:
                if '__main__' in sys.modules:
                    del sys.modules['__main__']
                SourceFileLoader('__main__', path).load_module()
            except raises:
                return output.getvalue()
            except SystemExit as e:
                if e.args != (0,):
                    raise
            if raises is not DummyException:
                raise AssertionError("{} not raised".format(raises))
            return output.getvalue()
    finally:
        sys.argv = old_args
        # The next 3 lines seem to fix weird cyclic-reference issues
        if '__main__' in sys.modules:
            sys.modules['__main__'].__dict__.clear()
            sys.modules.pop('__main__', None)
        gc.collect()


@contextmanager
def make_file(contents=None):
    """Context manager providing name of a file containing given contents."""
    with NamedTemporaryFile(mode='wt', encoding='utf-8', delete=False) as f:
        if contents:
            f.write(contents)
    try:
        yield f.name
    finally:
        os.remove(f.name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
