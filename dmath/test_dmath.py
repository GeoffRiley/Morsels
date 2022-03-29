from contextlib import contextmanager, redirect_stdout, redirect_stderr
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from io import StringIO
from pathlib import Path
import shlex
import sys
import unittest


class DMathTests(unittest.TestCase):
    """Tests for dmath.py"""
    def setUp(self):
        self.patched_date = patch_date(2018, 9, 3, 10, 30)
        self.set_date = self.patched_date.__enter__()

    def tearDown(self):
        self.patched_date.__exit__(None, None, None)

    def assertRun(self, arguments, output):
        self.assertEqual(run_program(f"dmath.py {arguments}"), f"{output}\n")

    def test_positive_numbers(self):
        self.assertEqual(run_program("dmath.py 10"), "2018-09-13\n")
        self.assertEqual(run_program("dmath.py 1"), "2018-09-04\n")
        self.assertEqual(run_program("dmath.py 130"), "2019-01-11\n")
        self.assertEqual(run_program("dmath.py 365"), "2019-09-03\n")
        self.assertEqual(run_program("dmath.py 366"), "2019-09-04\n")

    def test_different_date(self):
        self.set_date(2020, 1, 1)
        self.assertEqual(run_program("dmath.py 72"), "2020-03-13\n")
        self.assertEqual(run_program("dmath.py 365"), "2020-12-31\n")
        self.assertEqual(run_program("dmath.py 366"), "2021-01-01\n")

    def test_negative_number(self):
        self.assertEqual(run_program("dmath.py -10"), "2018-08-24\n")
        self.assertEqual(run_program("dmath.py -1"), "2018-09-02\n")
        self.assertEqual(run_program("dmath.py -130"), "2018-04-26\n")
        self.assertEqual(run_program("dmath.py -365"), "2017-09-03\n")
        self.assertEqual(run_program("dmath.py -366"), "2017-09-02\n")

    def test_non_integers_fail(self):
        out, err = run_program("dmath.py 10.5", stderr=True, raises=SystemExit)
        self.assertEqual(out, "")
        self.assertIn("error", err.casefold())
        out, err = run_program("dmath.py a", stderr=True, raises=SystemExit)
        self.assertEqual(out, "")
        self.assertIn("error", err.casefold())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_date_and_number(self):
        self.set_date(2019, 6, 20)

        self.assertRun("2018-09-03 10", "2018-09-13")
        self.assertRun("2018-09-03 1", "2018-09-04")
        self.assertRun("2018-09-03 130", "2019-01-11")
        self.assertRun("2018-09-03 365", "2019-09-03")
        self.assertRun("2018-09-03 366", "2019-09-04")
        self.assertRun("2018-09-03 -10", "2018-08-24")
        self.assertRun("2018-09-03 -1", "2018-09-02")
        self.assertRun("2018-09-03 -130", "2018-04-26")
        self.assertRun("2018-09-03 -365", "2017-09-03")
        self.assertRun("2018-09-03 -366", "2017-09-02")

        self.assertRun("2020-01-01 72", "2020-03-13")
        self.assertRun("2020-01-01 365", "2020-12-31")
        self.assertRun("2020-01-01 366", "2021-01-01")

        # Non-date shows error
        out, err = run_program(
            "dmath.py 09/03/2020 10",
            stderr=True,
            raises=SystemExit,
        )
        self.assertEqual(out, "")
        self.assertIn("error", err.casefold())
        out, err = run_program("dmath.py a 10", stderr=True, raises=SystemExit)
        self.assertEqual(out, "")
        self.assertIn("error", err.casefold())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_two_dates(self):
        self.assertRun("2020-08-04 2020-10-05", "62")
        self.assertRun("2020-10-05 2020-08-04", "-62")
        self.assertRun("2018-09-03 2020-10-05", "763")
        self.assertRun("2018-09-03 2020-01-01", "485")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_numeric_expressions(self):
        self.set_date(2019, 6, 20)

        self.assertRun("2018-09-03 5+5", "2018-09-13")
        self.assertRun("2018-09-03 7*20", "2019-01-21")
        self.assertRun("2018-09-03 26*-5", "2018-04-26")
        self.assertRun("2018-09-03 -365-1", "2017-09-02")
        self.assertRun("2020-01-01 6*6*2", "2020-03-13")

        # Invalid expressions
        out, err = run_program(
            "dmath.py 2018-09-03 5==5",
            stderr=True,
            raises=SystemExit,
        )
        self.assertEqual(out, "")
        self.assertIn("error", err.casefold())
        out, err = run_program(
            "dmath.py 2018-09-03 7@20",
            stderr=True,
            raises=SystemExit,
        )
        self.assertEqual(out, "")
        self.assertIn("error", err.casefold())
        out, err = run_program(
            "dmath.py 2018-09-03 (5).real",
            stderr=True,
            raises=SystemExit,
        )
        self.assertEqual(out, "")
        self.assertIn("error", err.casefold())
        out, err = run_program(
            "dmath.py 2018-09-03 5/6",
            stderr=True,
            raises=SystemExit,
        )
        self.assertEqual(out, "")
        self.assertIn("error", err.casefold())


class DummyException(Exception):
    """No code will ever raise this exception."""


try:
    DIRECTORY = Path(__file__).resolve().parent
except NameError:
    DIRECTORY = Path.cwd()


def run_program(arguments, raises=DummyException, stderr=False):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.
    """
    path, *args = shlex.split(arguments, posix=False)
    path = str(DIRECTORY / path)
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            error = StringIO() if stderr else output
            with redirect_stderr(error):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    loader = SourceFileLoader('__main__', path)
                    spec = spec_from_loader(loader.name, loader)
                    module = module_from_spec(spec)
                    sys.modules['__main__'] = module
                    loader.exec_module(module)
                except raises:
                    pass
                except SystemExit as e:
                    if e.args != (0, ):
                        raise SystemExit(output.getvalue()) from e
                else:
                    if raises is not DummyException:
                        raise AssertionError("{} not raised".format(raises))
                if stderr:
                    return output.getvalue(), error.getvalue()
                else:
                    return output.getvalue()
    finally:
        sys.argv = old_args


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

    def set_date(year, month, day, *rest):
        nonlocal date_args, time_args
        date_args = year, month, day
        time_args = rest

    FakeDate.__name__ = 'date'
    FakeDateTime.__name__ = 'datetime'
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
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
