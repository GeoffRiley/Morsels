from contextlib import contextmanager, redirect_stdout
from io import StringIO
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import os
from pathlib import Path
import shlex
import sys
from textwrap import dedent
from tempfile import NamedTemporaryFile
import unittest
import warnings


class INI2CSV(unittest.TestCase):

    """Tests for ini2csv.py"""

    maxDiff = None

    def test_two_groups(self):
        contents = dedent("""
            [*.py]
            indent_style = space
            indent_size = 4

            [*.js]
            indent_style = space
            indent_size = 2
        """).lstrip()
        expected = dedent("""
            *.py,indent_style,space
            *.py,indent_size,4
            *.js,indent_style,space
            *.js,indent_size,2
        """).lstrip()
        with make_file(contents) as ini_file, make_file() as csv_file:
            stdout = run_program(f'ini2csv.py {ini_file} {csv_file}')
            self.assertEqual(stdout, '')
            with open(csv_file) as csv:
                output = csv.read()
        self.assertEqual(expected, output)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_collapsed(self):
        contents = dedent("""
            [*.py]
            indent_style = space
            indent_size = 4

            [*.js]
            indent_style = space
            indent_size = 2
        """).lstrip()
        expected = dedent("""
            header,indent_style,indent_size
            *.py,space,4
            *.js,space,2
        """).lstrip()
        with make_file(contents) as ini_file, make_file() as csv_file:
            run_program(f'ini2csv.py --collapsed {ini_file} {csv_file}')
            with open(csv_file) as csv:
                output = csv.read()
        self.assertEqual(expected, output)


try:
    DIRECTORY = Path(__file__).resolve().parent
except NameError:
    DIRECTORY = Path.cwd()


def run_program(arguments):  # sourcery skip: extract-method
    """Run program at given path with given arguments."""
    arguments = arguments.replace('\\', '\\\\')
    path, *args = shlex.split(arguments)
    path = str(DIRECTORY / path)
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    warnings.simplefilter("ignore", ResourceWarning)
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            try:
                if '__main__' in sys.modules:
                    del sys.modules['__main__']
                loader = SourceFileLoader('__main__', path)
                spec = spec_from_loader(loader.name, loader)
                module = module_from_spec(spec)
                sys.modules['__main__'] = module
                loader.exec_module(module)

            except SystemExit as e:
                if e.args != (0,):
                    raise
            finally:
                if '__main__' in sys.modules:
                    sys.modules['__main__'].__dict__.clear()
                sys.modules.pop('__main__', None)  # Closes any open files
            return output.getvalue()
    finally:
        sys.argv = old_args


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
