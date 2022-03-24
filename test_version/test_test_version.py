from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from importlib.machinery import SourceFileLoader
from pathlib import Path
import os
import os.path
import sys
from textwrap import dedent
from types import ModuleType
import unittest


class TestVersionTests(unittest.TestCase):
    """Tests for test_version.py."""

    just_init = """
        class Version:
            def __init__(self, version):
                if not isinstance(version, str):
                    raise TypeError("Version must be a string")
                self._parts = [int(p) for p in version.split('.')]
                if not (0 < len(self._parts) <= 3):
                    raise ValueError("Version must have 1-3 numeric parts")
                self._parts += [0] * (3-len(self._parts))
    """

    with_comparisons = just_init + """
            def __eq__(self, other):
                if isinstance(other, Version):
                    return self._parts == other._parts
                return NotImplemented

            def __lt__(self, other):
                if isinstance(other, Version):
                    return self._parts < other._parts
                return NotImplemented
            def __gt__(self, other):
                if isinstance(other, Version):
                    return self._parts > other._parts
                return NotImplemented
            def __le__(self, other):
                if isinstance(other, Version):
                    return self._parts <= other._parts
                return NotImplemented
            def __ge__(self, other):
                if isinstance(other, Version):
                    return self._parts >= other._parts
                return NotImplemented
    """

    repr_method = """
            def __repr__(self):
                return "Version({!r})".format(str(self))
    """
    str_method = """
            def __str__(self):
                return "{0}.{1}.{2}".format(*self._parts)
    """

    missing_str = with_comparisons + repr_method

    missing_repr = with_comparisons + str_method

    without_comparisons = just_init + repr_method + str_method

    fully_working = with_comparisons + repr_method + str_method

    eq_and_ne_true = fully_working + """

            def __eq__(self, other):
                return True
            def __ne__(self, other):
                return True
    """

    lt_always_true = fully_working + """
            def __lt__(self, other):
                if isinstance(other, Version):
                    return True
                return NotImplemented
    """

    gt_always_true = fully_working + """
            def __gt__(self, other):
                if isinstance(other, Version):
                    return True
                return NotImplemented
    """

    le_always_true = fully_working + """
            def __le__(self, other):
                if isinstance(other, Version):
                    return True
                return NotImplemented
    """

    ge_always_true = fully_working + """
            def __ge__(self, other):
                if isinstance(other, Version):
                    return True
                return NotImplemented
    """

    lt_with_other_type_fails = fully_working + """
            def __lt__(self, other):
                return self._parts < other._parts
    """

    ge_with_other_type_fails = fully_working + """
            def __ge__(self, other):
                return self._parts >= other._parts
    """

    eq_with_other_type_fails = fully_working + """
            def __eq__(self, other):
                return self._parts == other._parts
    """

    empty_allowed = fully_working + """
            def __init__(self, version):
                if not isinstance(version, str):
                    raise TypeError("Version must be a string")
                self._parts = [int(p or 0) for p in version.split('.')]
                self._parts += [0] * (3-len(self._parts))
                if not (0 < len(self._parts) <= 3):
                    raise ValueError("Version must have 1-3 numeric parts")
    """

    missing_components_with_broken_eq = fully_working + """
            def __init__(self, version):
                if not isinstance(version, str):
                    raise TypeError("Version must be a string")
                self._parts = [int(p) for p in version.split('.')]
                if not (0 < len(self._parts) <= 3):
                    raise ValueError("Version must have 1-3 numeric parts")
            def __str__(self):
                parts = self._parts + [0] * (3-len(self._parts))
                return "{0}.{1}.{2}".format(*parts)
    """

    def make_module(self, code, *, name="version", docstring=None):
        module = ModuleType(name, docstring)
        module.__file__ = name + ".py"
        exec(code, module.__dict__)
        sys.modules[name] = module
        return module

    def ensure_success(self, module_code):
        module_code = dedent(module_code)
        self.make_module(module_code)
        self.assertRegex(
            run_program('test_version.py'),
            r'OK$',
            f"\nThis module failed but should have passed!\n{module_code}",
        )

    def ensure_failure(self, module_code):
        module_code = dedent(module_code)
        self.make_module(module_code)
        self.assertRegex(
            run_program('test_version.py'),
            r'FAILED .*$',
            f"\nThis module passed but should have failed!\n{module_code}",
        )

    def test_fully_working_version_passes(self):
        self.ensure_success(self.fully_working)

    def test_missing_string_representations(self):
        # Missing __repr__
        self.ensure_failure(self.missing_repr)

        # Missing __str__
        self.ensure_failure(self.missing_str)

    def test_empty_version_should_not_be_allowed(self):
        self.ensure_failure(self.empty_allowed)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_equality_works_and_version_components_default_to_zero(self):
        self.ensure_failure(self.without_comparisons)
        self.ensure_failure(self.missing_components_with_broken_eq)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_less_than(self):
        self.ensure_failure(self.lt_always_true)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_other_comparisons(self):
        # == and != shouldn't just return True
        self.ensure_failure(self.eq_and_ne_true)

        # > can't just return True
        self.ensure_failure(self.gt_always_true)

        # <= and >= can't just return True
        self.ensure_failure(self.le_always_true)
        self.ensure_failure(self.ge_always_true)

        # <, >=, == shouldn't raise ValueError with other types
        self.ensure_failure(self.lt_with_other_type_fails)
        self.ensure_failure(self.ge_with_other_type_fails)
        self.ensure_failure(self.eq_with_other_type_fails)


class DummyException(Exception):
    """No code will ever raise this exception."""


try:
    DIRECTORY = Path(__file__).resolve().parent
except NameError:
    DIRECTORY = Path.cwd()


def run_program(path, args=[], raises=DummyException):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.
    """
    path = str(DIRECTORY.joinpath(path))
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            with redirect_stderr(output):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    SourceFileLoader('__main__', path).load_module()
                except raises:
                    return output.getvalue()
                except SystemExit:
                    return output.getvalue()
                if raises is not DummyException:
                    raise AssertionError("{} not raised".format(raises))
                return output.getvalue()
    finally:
        sys.argv = old_args


if __name__ == "__main__":
    unittest.main(verbosity=2)
