"""Test helpers"""
from contextlib import contextmanager
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from pathlib import Path
import os
from io import StringIO
import imp
from importlib.machinery import SourceFileLoader
import sys
from tempfile import NamedTemporaryFile
import unittest


DIR_PATH = Path(__file__).parent


class DummyException(BaseException):
    """This should never be raised."""


def run_program(program, args=[], raises=DummyException, stderr=False):
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    try:
        module_path = DIR_PATH / 'modules' / program
        sys.argv = [program] + args
        with redirect_stdout(StringIO()) as output:
            error = StringIO() if stderr else output
            with redirect_stderr(error):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    SourceFileLoader('__main__', str(module_path)).load_module()
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


def import_module(module, args=[]):
    path = 'modules/{module}.py'.format(module=module)
    return imp.load_source(module, path)


@contextmanager
def cd(new_directory):
    original_directory = os.getcwd()
    os.chdir(os.path.expanduser(new_directory))
    try:
        yield
    finally:
        os.chdir(original_directory)


@contextmanager
def make_file(contents=None):
    with NamedTemporaryFile(mode='wt', delete=False) as f:
        if contents:
            f.write(contents)
    try:
        yield f.name
    finally:
        os.remove(f.name)


@contextmanager
def capture_stdin(data):
    old_stdin, sys.stdin = sys.stdin, StringIO()
    try:
        sys.stdin.write(data)
        sys.stdin.seek(0)
        yield sys.stdin
    finally:
        sys.stdin = old_stdin


def error_message():
    print("Cannot run {} from the command-line.".format(sys.argv[0]))
    print()
    print("Run python test.py <your_exercise_name> instead")


class ModuleTestCase(unittest.TestCase):

    """TestCase for module/program tests."""

    @classmethod
    def setUpClass(cls):
        if not hasattr(cls, 'module_path'):
            raise NotImplementedError('Test needs "module_path" attribute')
