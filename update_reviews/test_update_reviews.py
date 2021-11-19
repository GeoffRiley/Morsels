from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import os
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
import unittest


class UpdateReviewsTests(unittest.TestCase):

    """Tests for update_reviews.py."""

    maxDiff = None

    def run_program(self, file1_text, file2_text, *extra_args):
        """
        Make 2 files and call update_reviews.py with them.

        Returns the updated text of the second file and captured stdout.
        """
        if not file1_text.endswith('\n'):
            file1_text += "\n"
        if not file2_text.endswith('\n'):
            file2_text += "\n"
        with make_file(file1_text) as old, make_file(file2_text) as new:
            args = [old, new, *extra_args]
            output = run_program('update_reviews.py', args=args)
            self.assertEqual(
                Path(new).read_text(),
                file2_text,
                'new file is unchanged',
            )
            updated_text = Path(old).read_text()
        return updated_text, output

    def test_just_header_rows(self):
        contents = "Name,Price,Street,City,State,Comments\n"
        updated_text, output = self.run_program(contents, contents)
        self.assertEqual(contents, updated_text)
        self.assertEqual("Added 0 row(s)\n", output)

    def test_no_new_rows(self):
        text1 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's Hot Chicken,$$,112 19th Ave S,Nashville,TN,",
        ])
        text2 = "\n".join([
            "Name,Price,Street,City,State,Comments",
        ])
        updated_text, output = self.run_program(text1, text2)
        self.assertEqual(updated_text.splitlines(), text1.splitlines())
        self.assertEqual("Added 0 row(s)\n", output)

    def test_only_new_rows(self):
        text1 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's Hot Chicken,$$,112 19th Ave S,Nashville,TN,",
        ])
        text2 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
        ])
        expected = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's Hot Chicken,$$,112 19th Ave S,Nashville,TN,",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
        ])
        updated_text, output = self.run_program(text1, text2)
        self.assertEqual(updated_text.splitlines(), expected.splitlines())
        self.assertEqual("Added 1 row(s)\n", output)

    def test_some_duplicate_rows(self):
        text1 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's Hot Chicken,$$,112 19th Ave S,Nashville,TN,very good",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
        ])
        text2 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Hattie B's Hot Chicken,$$,112 19th Ave S,Nashville,TN,",
        ])
        expected = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's Hot Chicken,$$,112 19th Ave S,Nashville,TN,very good",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
        ])
        updated_text, output = self.run_program(text1, text2)
        self.assertEqual(updated_text.splitlines(), expected.splitlines())
        self.assertEqual("Added 1 row(s)\n", output)

    def test_many_rows_and_some_duplicate_restaurants(self):
        text1 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Stubb's Bar-B-Q,$,801 Red River St,Austin,TX,",
            "Texas Chili Parlor,$,1409 Lavaca St,Austin,TX,",
            "Bolton's Spicy Chicken & Fish,$$,624 Main St,Nashville,TN,",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,very good",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Killer Burger,$,500 SW 3rd Ave,Portland,OR,peanut butter burger",
        ])
        text2 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
            "John's Water Ice,$,701 Christian St,Philadelphia,PA,",
            "Han Dynasty,$$,3711 Market St,Philadelphia,PA,",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,Bolton's was better",
            "Best Bagel & Coffee,$,225 W 35th St,New York,NY,",
            "Santa Panza,$,1079 Broadway,New York,NY,",
        ])
        expected = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Stubb's Bar-B-Q,$,801 Red River St,Austin,TX,",
            "Texas Chili Parlor,$,1409 Lavaca St,Austin,TX,",
            "Bolton's Spicy Chicken & Fish,$$,624 Main St,Nashville,TN,",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,very good",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Killer Burger,$,500 SW 3rd Ave,Portland,OR,peanut butter burger",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
            "John's Water Ice,$,701 Christian St,Philadelphia,PA,",
            "Han Dynasty,$$,3711 Market St,Philadelphia,PA,",
            "Best Bagel & Coffee,$,225 W 35th St,New York,NY,",
            "Santa Panza,$,1079 Broadway,New York,NY,",
        ])
        updated_text, output = self.run_program(text1, text2)
        self.assertEqual(updated_text.splitlines(), expected.splitlines())
        self.assertEqual("Added 5 row(s)\n", output)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_use_name_and_address_as_unique_identifiers(self):
        text1 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's Hot Chicken,$$,112 19th Ave S,Nashville,TN,very good",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
            "Han Dynasty,$$,3711 Market St,Philadelphia,PA,",
        ])
        text2 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Hattie B's Hot Chicken,$$,5209 Charlotte Pike,Nashville,TN,",
            "Han Dynasty,$$,90 3rd Ave,New York,NY,",
        ])
        expected = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's Hot Chicken,$$,112 19th Ave S,Nashville,TN,very good",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
            "Han Dynasty,$$,3711 Market St,Philadelphia,PA,",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Hattie B's Hot Chicken,$$,5209 Charlotte Pike,Nashville,TN,",
            "Han Dynasty,$$,90 3rd Ave,New York,NY,",
        ])
        updated_text, output = self.run_program(text1, text2)
        self.assertEqual(updated_text.splitlines(), expected.splitlines())
        self.assertEqual("Added 3 row(s)\n", output)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_update_argument(self):
        text1 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,very good",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
        ])
        text2 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Bolton's Spicy Chicken & Fish,$$,624 Main St,Nashville,TN,",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,Bolton's was better",
        ])
        expected = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,Bolton's was better",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Bolton's Spicy Chicken & Fish,$$,624 Main St,Nashville,TN,",
        ])
        updated_text, output = self.run_program(text1, text2, '--update')
        self.assertEqual(updated_text.splitlines(), expected.splitlines())
        self.assertEqual(
            "Added 2 row(s)\n"
            "Updated 1 row(s)\n",
            output,
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_sort_argument(self):
        text1 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Stubb's Bar-B-Q,$,801 Red River St,Austin,TX,",
            "Texas Chili Parlor,$,1409 Lavaca St,Austin,TX,",
            "Bolton's Spicy Chicken & Fish,$$,624 Main St,Nashville,TN,",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,very good",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Killer Burger,$,500 SW 3rd Ave,Portland,OR,peanut butter burger",
        ])
        text2 = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
            "John's Water Ice,$,701 Christian St,Philadelphia,PA,",
            "Han Dynasty,$$,3711 Market St,Philadelphia,PA,",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,Bolton's was better",
            "Best Bagel & Coffee,$,225 W 35th St,New York,NY,",
            "Han Dynasty,$$,90 3rd Ave,New York,NY,",
            "Santa Panza,$,1079 Broadway,New York,NY,",
        ])
        expected = "\n".join([
            "Name,Price,Street,City,State,Comments",
            "Best Bagel & Coffee,$,225 W 35th St,New York,NY,",
            "Han Dynasty,$$,90 3rd Ave,New York,NY,",
            "Santa Panza,$,1079 Broadway,New York,NY,",
            "Killer Burger,$,500 SW 3rd Ave,Portland,OR,peanut butter burger",
            "Pok Pok,$$,3226 SE Division St,Portland,OR,",
            "Han Dynasty,$$,3711 Market St,Philadelphia,PA,",
            "Jim's Steaks,$,400 South St,Philadelphia,PA,I want to come back",
            "John's Water Ice,$,701 Christian St,Philadelphia,PA,",
            "Bolton's Spicy Chicken & Fish,$$,624 Main St,Nashville,TN,",
            "Hattie B's,$$,112 19th Ave S,Nashville,TN,very good",
            "Stubb's Bar-B-Q,$,801 Red River St,Austin,TX,",
            "Texas Chili Parlor,$,1409 Lavaca St,Austin,TX,",
        ])
        updated_text, output = self.run_program(text1, text2, '--sort')
        self.assertEqual(updated_text.splitlines(), expected.splitlines())
        self.assertEqual("Added 6 row(s)\n", output)


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
                    if e.args != (0,):
                        raise SystemExit(output.getvalue()) from e
                if raises is not DummyException:
                    raise AssertionError("{} not raised".format(raises))
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
