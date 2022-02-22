import os
import unittest
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent

from lines import count_lines


def undent(text):
    return dedent(text).lstrip("\n")


class CountLinesTests(unittest.TestCase):
    """Tests for count_lines."""

    file1 = "tau = 6.283185307179586\n"

    file2 = "print('hello world')"

    file3 = undent("""
        print('line 1')

        print('line 2')

    """)

    file4 = ""

    file5 = undent("""
        from decimal import Decimal

        while True:
            try:
                n = Decimal(input("What is your favorite number?"))
            except ValueError:
                print("That's not a number!")
            else:
                print(f"Oh {n} is a lovely number!")
    """)

    file6 = undent("""
        2 + 3
    """)

    file7 = undent("""
        This project
        ============

        This project is lovely.

        I'm not sure what it does, but I'm glad it exists.
        I'm sure you'll enjoy it.

        Pull requests accepted.
    """)

    @contextmanager
    def make_files(self, files):
        with TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            for name, contents in files:
                filename = (tmp_dir / name)
                filename.parent.mkdir(parents=True, exist_ok=True)
                filename.write_text(contents)
            yield tmp_dir

    def test_two_single_line_files(self):
        with self.make_files([
            ('a.py', self.file1),
            ('b.py', self.file2),
        ]) as directory:
            response = count_lines(str(directory))
        self.assertEqual(set(response.keys()), {'py'})
        self.assertEqual(response['py'].files, 2)
        self.assertEqual(response['py'].lines, 2)
        self.assertEqual(response['py'].non_blank, 2)

    def test_empty_file(self):
        with self.make_files([
            ('empty.py', self.file4),
        ]) as directory:
            response = count_lines(str(directory))
        self.assertEqual(set(response.keys()), {'py'})
        self.assertEqual(response['py'].files, 1)
        self.assertEqual(response['py'].lines, 0)
        self.assertEqual(response['py'].non_blank, 0)

    def test_file_with_blank_lines(self):
        with self.make_files([
            ('with_blanks.py', self.file3),
        ]) as directory:
            response = count_lines(str(directory))
        self.assertEqual(set(response.keys()), {'py'})
        self.assertEqual(response['py'].files, 1)
        self.assertEqual(response['py'].lines, 4)
        self.assertEqual(response['py'].non_blank, 2)

    def test_both_py_and_pyc_files(self):
        with self.make_files([
            ('file1.py', self.file1),
            ('file2.py', self.file2),
            ('file3.pyc', self.file3),
            ('file5.py', self.file5),
        ]) as directory:
            response = count_lines(str(directory))
        self.assertEqual(set(response.keys()), {'py'})
        self.assertEqual(response['py'].files, 3)
        self.assertEqual(response['py'].lines, 11)
        self.assertEqual(response['py'].non_blank, 10)

    def test_find_files_recursively(self):
        with self.make_files([
            ('raul/__init__.py', self.file1),
            ('raul/viola.py', self.file3),
            ('raul/lena.pyc', self.file7),
            ('irene/__init__.py', self.file4),
            ('irene/rosa/__init__.py', self.file5),
            ('irene/rosa/mark.py', self.file6),
            ('irene/rosa/rita.py', self.file2),
        ]) as directory:
            response = count_lines(str(directory))
        self.assertEqual(set(response.keys()), {'py'})
        self.assertEqual(response['py'].files, 6)
        self.assertEqual(response['py'].lines, 16)
        self.assertEqual(response['py'].non_blank, 13)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_extensions_argument(self):
        with self.make_files([
            ('file1.js', self.file1),
            ('file2.html', self.file2),
            ('file3.txt', self.file3),
            ('__init__.py', self.file4),
            ('file5.py', self.file5),
            ('file6.bin', self.file6),
            ('README.md', self.file7),
        ]) as directory:
            response = count_lines(
                str(directory),
                extensions=['js', 'md', 'py', 'jsx'],
            )
            response2 = count_lines(str(directory))

        self.assertEqual(set(response.keys()), {'js', 'md', 'py'})
        self.assertEqual(response['js'].files, 1)
        self.assertEqual(response['js'].lines, 1)
        self.assertEqual(response['js'].non_blank, 1)
        self.assertEqual(response['md'].files, 1)
        self.assertEqual(response['md'].lines, 9)
        self.assertEqual(response['md'].non_blank, 6)
        self.assertEqual(response['py'].files, 2)
        self.assertEqual(response['py'].lines, 9)
        self.assertEqual(response['py'].non_blank, 8)

        # Default extensions are js, md, py, html
        self.assertEqual(set(response2.keys()), {'js', 'md', 'py', 'html'})
        self.assertEqual(response2['html'].files, 1)
        self.assertEqual(response2['html'].lines, 1)
        self.assertEqual(response2['html'].non_blank, 1)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_reading_directories_and_permission_errors(self):
        with self.make_files([
            ('file1.js', self.file1),
            ('file2.md', self.file2),
            ('file3.py', self.file3),
            ('__init__.py', self.file4),
            ('file5.py', self.file5),
            ('README.md', self.file7),
        ]) as directory:
            (directory / 'file4.py').mkdir()
            unreadable_files = [
                (directory / 'file1.js'),
                (directory / 'file2.md'),
            ]
            with force_permission_errors(*unreadable_files):
                response = count_lines(str(directory), extensions=['md', 'py'])
        self.assertEqual(set(response.keys()), {'md', 'py'})
        self.assertEqual(response['md'].files, 1)
        self.assertEqual(response['md'].lines, 9)
        self.assertEqual(response['md'].non_blank, 6)
        self.assertEqual(response['py'].files, 3)
        self.assertEqual(response['py'].lines, 13)
        self.assertEqual(response['py'].non_blank, 10)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_ignored_attribute(self):
        with self.make_files([
            ('file1.js', self.file1),
            ('file2.md', self.file2),
            ('file3.py', self.file3),
            ('__init__.py', self.file4),
            ('file5.txt', self.file5),
            ('README.md', self.file7),
        ]) as directory:
            (directory / 'file4.py').mkdir()
            unreadable_files = [
                (directory / 'file1.js'),
                (directory / 'file2.md'),
            ]
            with force_permission_errors(*unreadable_files):
                counts = count_lines(str(directory), extensions=['md', 'py'])
        self.assertEqual(len(counts.ignored), 3)
        ignored = sorted(counts.ignored)
        self.assertEqual(
            [Path(x[0]).name for x in ignored],
            ['file1.js', 'file2.md', 'file5.txt'],
        )
        self.assertEqual(ignored[0][1], ignored[2][1], "js and txt ignored")
        self.assertNotEqual(ignored[0][1], ignored[1][1], "file2.md had error")


@contextmanager
def force_permission_errors(*paths):
    if os.name == 'nt':
        # Windows hack: opening directory raises PermissionError
        # https://bugs.python.org/issue43095
        for path in paths:
            path.unlink()
            path.mkdir()
    else:
        # Make files write-only
        for path in paths:
            path.chmod(0o200)
    yield


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    import sys
    from platform import python_version
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
