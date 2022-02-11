from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import os
import sys
from tempfile import TemporaryDirectory
import unittest

from pattern_rename import scan, format


class ScanTests(unittest.TestCase):
    """Tests for scan"""
    def test_scan_one_letter(self):
        self.assertEqual(scan("%X.py", "hello.py"), {'X': "hello"})

    def test_scan_two_letters(self):
        self.assertEqual(
            scan("%A/%B.txt", "directory/file.txt"),
            {
                'A': "directory",
                'B': "file"
            },
        )

    def test_scan_lots_of_letters(self):
        expected = {
            'A': "Bill Withers",
            'B': "Just As I Am",
            'N': "01",
            'T': "Harlem",
        }
        parts = scan(
            "%A - %B/%N - %T.mp3",
            "Bill Withers - Just As I Am/01 - Harlem.mp3",
        )
        self.assertEqual(parts, expected)
        parts = scan(
            "%A/%B/%N %T.mp3",
            "Bill Withers/Just As I Am/01 Harlem.mp3",
        )
        self.assertEqual(parts, expected)

    def test_scan_non_matching(self):
        self.assertIsNone(scan("%A/%B.txt", "directory_file.txt"))
        self.assertIsNone(scan("%A/%B.txt", "directory/file.csv"))
        self.assertIsNone(scan("%A/%B.txt", "directory/file"))

    def test_partial_match(self):
        self.assertIsNone(scan("Music/%X.mp3", "subdirectory/Music/yes.mp3"))
        self.assertIsNone(scan("Music/%X.mp3", "Music/yes.mp3.incomplete"))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_patterns_with_symbols_and_conservative_matching(self):
        self.assertIsNone(scan("%A/%B.txt", "D/Ftxt"))
        self.assertEqual(
            scan("%N %T.mp3", "11 All Night.mp3"),
            {
                'N': "11",
                'T': "All Night"
            },
        )
        parts = scan(
            "%A/%B [%Y]/%N %T.mp3",
            "Janelle Monáe/Dirty Computer [2018]/10 I Like That.mp3",
        )
        self.assertEqual(
            parts, {
                'A': "Janelle Monáe",
                'B': "Dirty Computer",
                'Y': "2018",
                'N': "10",
                'T': "I Like That",
            })


class FormatTests(unittest.TestCase):
    """Tests for format"""
    def test_format_one_letter(self):
        self.assertEqual(format("%X.py", {'X': "hello"}), "hello.py")

    def test_format_two_letters(self):
        self.assertEqual(
            format("%A/%B.txt", {
                'A': "directory",
                'B': "file"
            }),
            "directory/file.txt",
        )

    def test_format_lots_of_letters(self):
        parts = {
            'A': "Bill Withers",
            'B': "Just As I Am",
            'N': "01",
            'T': "Harlem",
        }
        self.assertEqual(
            format("%A - %B/%N - %T.mp3", parts),
            "Bill Withers - Just As I Am/01 - Harlem.mp3",
        )
        self.assertEqual(
            format("%A/%B/%N %T.mp3", parts),
            "Bill Withers/Just As I Am/01 Harlem.mp3",
        )

    def test_format_with_incorrect_letters(self):
        with self.assertRaises(Exception):
            format("%A/%C.txt", {'A': "directory", 'B': "file"})

    def test_format_with_repeated_letters(self):
        self.assertEqual(
            format("%B_%A/%B.txt", {
                'A': "directory",
                'B': "file"
            }),
            "file_directory/file.txt",
        )

    def test_format_with_missing_letters(self):
        self.assertEqual(
            format("%B.txt", {
                'A': "directory",
                'B': "file"
            }),
            "file.txt",
        )


class CommandLineTestMixin:
    @contextmanager
    def make_files(self, filenames):
        with TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            for name in filenames:
                filename = (tmp_dir / name)
                filename.parent.mkdir(parents=True, exist_ok=True)
                filename.touch()
            cwd = os.getcwd()
            os.chdir(str(tmp_dir))
            try:
                yield
            finally:
                os.chdir(cwd)

    def get_expected_lines(self, input_files, output_files):
        return [
            'Moving "{x}" to "{y}"'.format(x=N(x), y=N(y))
            for x, y in zip(input_files, output_files)
        ]


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class CommandLineTests(CommandLineTestMixin, unittest.TestCase):
    """Tests for command-line interface"""

    maxDiff = None

    def test_rename_multiple_directories(self):
        input_files = [
            "Patti Smith - Horses/01 - Gloria.mp3",
            "Patti Smith - Horses/02 - Redondo Beach.mp3",
            "Patti Smith - Horses/03 - Birdland.mp3",
            "Patti Smith - Horses/04 - Free Money.mp3",
            "Patti Smith - Horses/05 - Kimberly.mp3",
            "Patti Smith - Horses/06 - Break It Up.mp3",
            "Patti Smith - Horses/07 - Land.mp3",
            "Patti Smith - Horses/08 - Elegie.mp3",
            "Tracy Chapman - Tracy Chapman/01 - Talkin' 'bout a Revolution.mp3",
            "Tracy Chapman - Tracy Chapman/02 - Fast Car.mp3",
            "Tracy Chapman - Tracy Chapman/03 - Across the Lines.mp3",
            "Tracy Chapman - Tracy Chapman/04 - Behind the Wall.mp3",
            "Tracy Chapman - Tracy Chapman/05 - Baby Can I Hold You.mp3",
            "Tracy Chapman - Tracy Chapman/06 - Mountains o' Things.mp3",
            "Tracy Chapman - Tracy Chapman/07 - She's Got Her Ticket.mp3",
            "Tracy Chapman - Tracy Chapman/08 - Why.mp3",
            "Tracy Chapman - Tracy Chapman/09 - For My Lover.mp3",
            "Tracy Chapman - Tracy Chapman/10 - If Not Now….mp3",
            "Tracy Chapman - Tracy Chapman/11 - For You.mp3",
        ]
        output_files = [
            "Patti Smith/Horses/01 Gloria.mp3",
            "Patti Smith/Horses/02 Redondo Beach.mp3",
            "Patti Smith/Horses/03 Birdland.mp3",
            "Patti Smith/Horses/04 Free Money.mp3",
            "Patti Smith/Horses/05 Kimberly.mp3",
            "Patti Smith/Horses/06 Break It Up.mp3",
            "Patti Smith/Horses/07 Land.mp3",
            "Patti Smith/Horses/08 Elegie.mp3",
            "Tracy Chapman/Tracy Chapman/01 Talkin' 'bout a Revolution.mp3",
            "Tracy Chapman/Tracy Chapman/02 Fast Car.mp3",
            "Tracy Chapman/Tracy Chapman/03 Across the Lines.mp3",
            "Tracy Chapman/Tracy Chapman/04 Behind the Wall.mp3",
            "Tracy Chapman/Tracy Chapman/05 Baby Can I Hold You.mp3",
            "Tracy Chapman/Tracy Chapman/06 Mountains o' Things.mp3",
            "Tracy Chapman/Tracy Chapman/07 She's Got Her Ticket.mp3",
            "Tracy Chapman/Tracy Chapman/08 Why.mp3",
            "Tracy Chapman/Tracy Chapman/09 For My Lover.mp3",
            "Tracy Chapman/Tracy Chapman/10 If Not Now….mp3",
            "Tracy Chapman/Tracy Chapman/11 For You.mp3",
        ]
        with self.make_files(input_files):
            output = run_program(
                'pattern_rename.py',
                [N('%A - %B/%N - %T.mp3'),
                 N('%A/%B/%N %T.mp3')],
            )
        self.assertEqual(
            sorted(output.splitlines()),
            self.get_expected_lines(input_files, output_files),
        )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class MoreCommandLineTests(CommandLineTestMixin, unittest.TestCase):
    def test_match_types(self):
        input_files = [
            "Patti Smith/Horses/01Gloria.MP3",
            "Patti Smith/Horses/02Redondo Beach.MP3",
            "Patti Smith/Horses/03Birdland.MP3",
        ]
        output_files = [
            "Patti Smith/Horses/01Gloria.mp3",
            "Patti Smith/Horses/02Redondo Beach.mp3",
            "Patti Smith/Horses/03Birdland.mp3",
        ]

        # Uppercase letters match everything but slash
        with self.make_files(input_files):
            output = run_program(
                'pattern_rename.py',
                [N('%A/%T.MP3'), N('%A/%T.mp3')],
            )
            self.assertEqual(output, "")
            output = run_program(
                'pattern_rename.py',
                [N('%A/%B/%T.MP3'), N('%A/%B/%T.mp3')],
            )
            self.assertEqual(
                sorted(output.splitlines()),
                self.get_expected_lines(input_files, output_files),
            )

        # Lowercase letters match everything but spaces and slashes
        with self.make_files(input_files):
            output = run_program(
                'pattern_rename.py',
                [N('%A/%B/%n%t.MP3'), N('%A/%B/%n%t.mp3')],
            )
            inputs = [input_files[0], input_files[2]]
            outputs = [output_files[0], output_files[2]]
            self.assertEqual(
                sorted(output.splitlines()),
                self.get_expected_lines(inputs, outputs),
            )

        # Digits match integers
        with self.make_files(input_files):
            output = run_program(
                'pattern_rename.py',
                [N('%A/%B/%0%T.MP3'), N('%A/%B/%0%T.mp3')],
            )
            self.assertEqual(
                sorted(output.splitlines()),
                self.get_expected_lines(input_files, output_files),
            )


def N(path_string):
    """Normalize path string based on operating system."""
    return str(Path(path_string))


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
    path = str(DIRECTORY / path)
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            with redirect_stderr(output):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    loader = SourceFileLoader('__main__', path)
                    spec = spec_from_loader(loader.name, loader)
                    module = module_from_spec(spec)
                    sys.modules['__main__'] = module
                    loader.exec_module(module)
                except raises:
                    return output.getvalue()
                except SystemExit as e:
                    if e.args != (0, ):
                        raise SystemExit(output.getvalue()) from e
                if raises is not DummyException:
                    raise AssertionError("{} not raised".format(raises))
                return output.getvalue()
    finally:
        sys.argv = old_args


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
