import os
from os.path import abspath, exists, dirname, realpath
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from cd import cd


class CDTests(unittest.TestCase):

    """Tests for cd."""

    def setUp(self):
        self.dirs = []
        os.chdir(self.get_temp_dir())

    def tearDown(self):
        for directory in self.dirs:
            rmtree(directory, ignore_errors=True)

    def get_temp_dir(self):
        """Return the canonical path to a new temporary directory."""
        directory = realpath(mkdtemp())
        self.dirs.append(directory)
        return directory

    def test_directory_changed(self):
        directory = self.get_temp_dir()
        original = os.getcwd()
        with cd(directory):
            self.assertEqual(abspath(os.getcwd()), abspath(directory))
        self.assertEqual(abspath(os.getcwd()), abspath(original))

    def test_changing_directory_still_works(self):
        directory = self.get_temp_dir()
        directory2 = self.get_temp_dir()
        original = os.getcwd()
        with cd(directory):
            self.assertEqual(abspath(os.getcwd()), abspath(directory))
            os.chdir(directory2)
            self.assertEqual(abspath(os.getcwd()), abspath(directory2))
        self.assertEqual(abspath(os.getcwd()), abspath(original))

    def test_no_directory_change(self):
        original = os.getcwd()
        with cd(original):
            self.assertEqual(abspath(os.getcwd()), abspath(original))
        self.assertEqual(abspath(os.getcwd()), abspath(original))

    def test_changes_even_with_exceptions(self):
        directory = self.get_temp_dir()
        original = os.getcwd()
        with self.assertRaises(ValueError):
            with cd(directory):
                raise ValueError
        self.assertEqual(abspath(os.getcwd()), abspath(original))
        with self.assertRaises(SystemExit):
            with cd(directory):
                raise SystemExit
        self.assertEqual(abspath(os.getcwd()), abspath(original))

    def test_reentrant(self):
        directory = self.get_temp_dir()
        directory2 = self.get_temp_dir()
        original = os.getcwd()
        with cd(directory):
            with cd(directory2):
                self.assertEqual(abspath(os.getcwd()), abspath(directory2))
            self.assertEqual(abspath(os.getcwd()), abspath(directory))
        self.assertEqual(abspath(os.getcwd()), abspath(original))

    def test_directory_not_deleted_afterward(self):
        directory = self.get_temp_dir()
        with cd(directory):
            self.assertTrue(exists(directory), "given directory was deleted!")
        self.assertTrue(exists(directory), "given directory was deleted!")
        with cd(directory):
            with open('hello.txt', mode='wt') as f:
                f.write('hello!')
            filename = abspath('hello.txt')
        self.assertTrue(exists(filename), "file in directory was deleted!")

    def test_initialization_before_context_entering(self):
        directory = self.get_temp_dir()
        new_original = self.get_temp_dir()
        old_original = os.getcwd()
        dirs = cd(directory)
        self.assertEqual(abspath(os.getcwd()), abspath(old_original))
        os.chdir(new_original)
        with dirs:
            self.assertEqual(abspath(os.getcwd()), abspath(directory))
        self.assertEqual(abspath(os.getcwd()), abspath(new_original))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_no_argument_given(self):
        original = os.getcwd()
        dirs = cd()
        with dirs:
            self.assertNotEqual(abspath(os.getcwd()), abspath(original))
            self.assertEqual(os.listdir(), [])
            with open('hello.txt', mode='wt') as f:
                f.write('hello!')
            full_path = abspath('hello.txt')
            self.assertNotEqual(dirname(full_path), abspath(original))
            with open(full_path, mode='rt') as f:
                self.assertEqual(f.read(), 'hello!')
        self.assertEqual(abspath(os.getcwd()), abspath(original))
        self.assertFalse(exists(full_path), "temporary directory not deleted")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_has_current_and_previous_attributes(self):
        directory = self.get_temp_dir()
        original = os.getcwd()
        with cd(directory) as dirs:
            self.assertEqual(abspath(original), abspath(str(dirs.previous)))
            self.assertEqual(abspath(directory), abspath(str(dirs.current)))
        self.assertEqual(abspath(original), abspath(str(dirs.previous)))
        self.assertEqual(abspath(directory), abspath(str(dirs.current)))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_enter_and_exit_methods(self):
        directory = self.get_temp_dir()
        new_original = self.get_temp_dir()
        old_original = os.getcwd()
        dirs = cd(directory)
        self.assertEqual(abspath(os.getcwd()), abspath(old_original))
        os.chdir(new_original)
        dirs.enter()
        self.assertEqual(abspath(os.getcwd()), abspath(directory))
        dirs.exit()
        self.assertEqual(abspath(os.getcwd()), abspath(new_original))


if __name__ == "__main__":
    unittest.main(verbosity=2)
