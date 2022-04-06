import re
import sys
import unittest
from collections import UserList
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from math import sqrt
from pathlib import Path

from debug_calls import debug_calls


def call_my_function(function):
    return function()


class DebugCallsTests(unittest.TestCase):
    """Tests for debug_calls."""
    def assertStdoutStart(self, stdout, line):
        self.assertEqual(stdout.getvalue()[:len(line)], line)

    def test_not_called_on_decoration_time(self):
        def my_func():
            raise AssertionError("Function called too soon")

        debug_calls(my_func)

    def test_prints_when_called(self):
        recordings = []

        @debug_calls
        def my_func():
            recordings.append('call')
            return len(recordings)

        self.assertEqual(recordings, [])
        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(my_func(), 1)
        self.assertStdoutStart(stdout, "my_func() called")
        self.assertEqual(recordings, ['call'])
        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(my_func(), 2)
        self.assertStdoutStart(stdout, "my_func() called")
        self.assertEqual(recordings, ['call', 'call'])

    def test_prints_arguments(self):
        recordings = []

        @debug_calls
        def my_func(*args, **kwargs):
            recordings.append((args, kwargs))
            return recordings

        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(
                my_func(1, 2, a=3),
                [((1, 2), {
                    'a': 3
                })],
            )
        self.assertStdoutStart(stdout, "my_func(1, 2, a=3) called")
        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(
                my_func('a', x='b'),
                [((1, 2), {
                    'a': 3
                }), (('a', ), {
                    'x': 'b'
                })],
            )

        self.assertStdoutStart(stdout, "my_func('a', x='b') called")

    def test_docstring_and_name_preserved(self):
        import pydoc
        decorated = debug_calls(example)
        self.assertIn('function example', str(decorated))
        documentation = pydoc.render_doc(decorated)
        self.assertIn('function example', documentation)
        self.assertIn('Example function.', documentation)
        self.assertIn('(a, b=True)', documentation)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_show_caller_name(self):
        @debug_calls
        def my_func(*args, **kwargs):
            return (args, kwargs)

        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(call_my_function(my_func), ((), {}))
        self.assertIn(
            "called by call_my_function",
            stdout.getvalue(),
        )
        self.assertNotIn("test_show_caller_name", stdout.getvalue())

        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(my_func(), ((), {}))
        self.assertIn("test_show_caller_name", stdout.getvalue())
        self.assertNotIn("call_my_function", stdout.getvalue())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_show_file_and_line(self):
        @debug_calls
        def my_func(*args, **kwargs):
            return (args, kwargs)

        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(call_my_function(my_func), ((), {}))
        self.assertIn("on line 14", stdout.getvalue())
        self.assertIn("in file", stdout.getvalue())
        self.assertIn("test_debug_calls.py", stdout.getvalue())

        from inspect import currentframe, getframeinfo

        target_line = getframeinfo(currentframe()).lineno + 1
        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(my_func(), ((), {}))
        line_on = tuple(re.findall(r"on line (\d+)", stdout.getvalue()))
        self.assertIn(line_on,
                      {(str(n), )
                       for n in range(target_line - 6, target_line + 6)})
        self.assertIn("in file", stdout.getvalue())
        self.assertIn(__file__, stdout.getvalue())

        class Point:
            def __init__(self, x, y):
                self.x, self.y = x, y

            @debug_calls
            def __iter__(self):
                yield self.x
                yield self.y

        with redirect_stdout(StringIO()) as stdout:
            self.assertEqual(UserList(Point(1, 2)), [1, 2])
        self.assertIn("in file", stdout.getvalue())
        self.assertIn(str(Path("collections/__init__.py")), stdout.getvalue())
        self.assertIn("on line", stdout.getvalue())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_break_conditionally(self):
        @debug_calls(set_break=True)
        def quadratic(a, b, c):
            x1 = -b / (2 * a)
            x2 = sqrt(b**2 - 4 * a * c) / (2 * a)
            return (x1 + x2), (x1 - x2)

        with redirect_stdout(StringIO()) as stdout:
            with patch_stdin("a == 0\n"):
                self.assertEqual(quadratic(1, 4, 3), (-1, -3))
        self.assertIn("Debug quadratic when?", stdout.getvalue())
        self.assertIn("quadratic(1, 4, 3) called", stdout.getvalue())
        self.assertIn("Condition not met: a == 0", stdout.getvalue())
        self.assertNotIn("args = (1, 4, 3)", stdout.getvalue())

        with redirect_stdout(StringIO()) as stdout:
            with patch_stdin("s\nargs\ns\ns\nc\n"):
                with self.assertRaises(ZeroDivisionError):
                    quadratic(0, 4, 3)
        self.assertNotIn("Debug quadratic when?", stdout.getvalue())
        self.assertIn("quadratic(0, 4, 3) called", stdout.getvalue())
        self.assertIn("Condition met: a == 0", stdout.getvalue())
        self.assertIn("a = 0\nb = 4\nc = 3\n", stdout.getvalue())
        self.assertIn("ZeroDivisionError", stdout.getvalue())

        with redirect_stdout(StringIO()) as stdout:
            with patch_stdin("\n"):
                with self.assertRaises(ValueError):
                    quadratic(4, 1, 3)
        self.assertNotIn("Debug quadratic when?", stdout.getvalue())
        self.assertIn("quadratic(4, 1, 3) called", stdout.getvalue())
        self.assertIn("Condition not met: a == 0", stdout.getvalue())
        self.assertNotIn("a = ", stdout.getvalue())
        self.assertNotIn("ZeroDivisionError", stdout.getvalue())


def example(a, b=True):
    """Example function."""
    print('hello world')


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
