import importlib.util
from io import BytesIO, StringIO, TextIOWrapper
import sys
import re
import unittest


class LenTests(unittest.TestCase):

    """Tests for len."""

    def test_objects_with_a_length(self):
        len = get_function('len')
        self.assertEqual(len([1, 2, 3]), 3)
        self.assertEqual(len({1, 2, 3}), 3)
        self.assertEqual(len({1: 2, 3: 4}), 2)
        self.assertEqual(len('hello'), 5)

    def test_objects_without_a_length(self):
        len = get_function('len')
        with self.assertRaisesRegex(TypeError, "len"):
            len(4.0)
        with self.assertRaisesRegex(TypeError, "int"):
            len(4)

        class A:
            pass
        with self.assertRaisesRegex(
            TypeError,
            "object of type 'A' has no len()",
        ):
            len(A())


class AllTests(unittest.TestCase):

    """Tests for all."""

    def test_with_list(self):
        all = get_function('all')
        self.assertFalse(all([True, False, 4, '']))
        self.assertFalse(all([True, True, 4, '']))
        self.assertTrue(all([True, True, 4, 'hi']))

    def test_with_generator(self):
        all = get_function('all')
        numbers = [3, 1, 5, 8]
        self.assertFalse(all(n > 5 for n in numbers))
        self.assertFalse(all(n > 1 for n in numbers))
        self.assertTrue(all(n > 0 for n in numbers))

    def test_short_circuit_logic_used(self):
        all = get_function('all')
        numbers = [3, 1, 5, 8]
        squares = (n**2 for n in numbers)
        self.assertFalse(all(n > 2 for n in squares))
        self.assertEqual(
            list(squares),
            [25, 64],
            "Generator not fully consumed unless necessary",
        )


class SumTests(unittest.TestCase):

    """Tests for sum."""

    def test_sum_of_empty_iterables(self):
        sum = get_function('sum')
        self.assertEqual(sum([]), 0)
        self.assertEqual(sum(()), 0)

    def test_sum_of_sequences(self):
        sum = get_function('sum')
        self.assertEqual(sum([1, 2, 3]), 6)
        self.assertEqual(sum((1, 2, 3, 4)), 10)

    def test_sum_of_non_sequences(self):
        sum = get_function('sum')
        self.assertEqual(sum({1, 2, 3}), 6)
        self.assertEqual(sum(n**2 for n in [4, 5, 6]), 77)

    def test_start_value(self):
        sum = get_function('sum')
        self.assertEqual(sum({1, 2, 3}, 3), 9)
        self.assertEqual(sum(iter([]), 5), 5)

    def test_summing_lists(self):
        sum = get_function('sum')
        self.assertEqual(sum([[1, 2], [3, 4]], []), [1, 2, 3, 4])

    def test_summing_strings(self):
        sum = get_function('sum')
        with self.assertRaisesRegex(TypeError, "strings .* ''.join.*"):
            sum([], '')


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class EnumerateTests(unittest.TestCase):

    """Tests for enumerate."""

    def test_enumerate_iterable(self):
        enumerate = get_function('enumerate')
        self.assertEqual(
            list(enumerate(['a', 'b', 'c'])),
            [(0, 'a'), (1, 'b'), (2, 'c')],
        )

    def test_enumerate_start_argument(self):
        enumerate = get_function('enumerate')
        self.assertEqual(
            list(enumerate(['a', 'b', 'c', 'd', 'e'], start=5)),
            [(5, 'a'), (6, 'b'), (7, 'c'), (8, 'd'), (9, 'e')],
        )

    def test_enumerate_is_lazy(self):
        enumerate = get_function('enumerate')
        squares = (n**2 for n in [7, 11, 13])
        self.assertEqual(next(enumerate(squares, start=1)), (1, 49))
        self.assertEqual(list(squares), [121, 169])


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class PrintTests(unittest.TestCase):

    """Tests for print."""

    def setUp(self):
        self.real_stdout = sys.stdout
        self.stdout = sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.real_stdout

    def get_stdout(self):
        return self.stdout.getvalue().replace("\r\n", "\n")

    def reset_stdout(self):
        self.stdout.seek(0)
        self.stdout.truncate()

    def test_print_one_argument(self):
        print = get_function('print')
        print("hi")
        print(4)
        self.assertEqual(self.get_stdout(), "hi\n4\n")

    def test_print_no_arguments(self):
        print = get_function('print')
        print()
        self.assertEqual(self.get_stdout(), '\n')

    def test_print_with_multiple_arguments(self):
        print = get_function('print')
        print('hello', 'there')
        print('I', 'have', 4, 'chickens')
        self.assertEqual(self.get_stdout(), 'hello there\nI have 4 chickens\n')
        self.reset_stdout()
        print(1, 2, 3, 4)
        self.assertEqual(self.get_stdout(), '1 2 3 4\n')

    def test_print_with_sep(self):
        print = get_function('print')
        print('hello', 'there', sep='\n')
        self.assertEqual(self.get_stdout(), 'hello\nthere\n')
        self.reset_stdout()
        print(1, 2, 3, 4, sep='-')
        self.assertEqual(self.get_stdout(), '1-2-3-4\n')
        self.reset_stdout()
        print('these', 'are', 'some', 'words', sep=', ')
        self.assertEqual(self.get_stdout(), 'these, are, some, words\n')
        self.reset_stdout()

    def test_print_default_separator(self):
        print = get_function('print')
        print(1, 2, 3, 4, sep=' ')
        self.assertEqual(self.get_stdout(), '1 2 3 4\n')
        self.reset_stdout()
        print('these', 'are', 'some', 'words', sep=None)
        self.assertEqual(self.get_stdout(), 'these are some words\n')

    def test_non_string_sep_and_end(self):
        print = get_function('print')
        with self.assertRaises(TypeError):
            print(b'Trey', b'Diane', sep=b' ')
        with self.assertRaises(TypeError):
            print('Trey', 'Diane', sep=4)
        with self.assertRaises(TypeError):
            print('Trey', 'Diane', end=4)
        with self.assertRaises(TypeError):
            print(b'Trey', sep=b' ', end=b'\n')

    def test_print_with_end(self):
        print = get_function('print')
        print(4, end='\n\n')
        print('hi', end='')
        self.assertEqual(self.get_stdout(), '4\n\nhi')
        self.reset_stdout()
        print(1, 2, 3, 4, end='')
        self.assertEqual(self.get_stdout(), '1 2 3 4')
        self.reset_stdout()
        print('these', 'are', 'some', 'words', end='\n')
        self.assertEqual(self.get_stdout(), 'these are some words\n')
        self.reset_stdout()
        print('a', 'b', sep='\n', end='\n\n')
        self.assertEqual(self.get_stdout(), 'a\nb\n\n')

    def test_default_end(self):
        print = get_function('print')
        print(1, 2, 3, 4, end='\n')
        self.assertEqual(self.get_stdout(), '1 2 3 4\n')
        self.reset_stdout()
        print('these', 'are', 'some', 'words', end=None)
        self.assertEqual(self.get_stdout(), 'these are some words\n')
        self.reset_stdout()
        print(4, end=None)
        self.assertEqual(self.get_stdout(), "4\n")
        self.reset_stdout()
        print(4, end="\n")
        self.assertEqual(self.get_stdout(), "4\n")

    def test_with_sep_and_end(self):
        print = get_function('print')
        print(*range(5), sep=",", end="!")
        self.assertEqual(self.get_stdout(), "0,1,2,3,4!")

    def test_writing_to_file(self):
        print = get_function('print')
        my_file = StringIO()
        print(*range(5), file=my_file)
        self.assertEqual(my_file.getvalue(), "0 1 2 3 4\n")
        self.assertEqual(self.get_stdout(), "")

    def test_flush_argument_with_file(self):
        print = get_function('print')

        # No flush with a buffered file doesn't write
        my_file = BufferedStringIO()
        print(*range(5), file=my_file)
        self.assertEqual(my_file.getvalue(), "")
        my_file.flush()
        self.assertEqual(my_file.getvalue(), "0 1 2 3 4\n")

        my_file = BufferedStringIO()
        print(*range(5), file=my_file, flush=True)
        self.assertEqual(my_file.getvalue(), "0 1 2 3 4\n")
        my_file.flush()
        self.assertEqual(my_file.getvalue(), "0 1 2 3 4\n")


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class NextTests(unittest.TestCase):

    """Tests for next."""

    def test_next_before_end(self):
        next = get_function('next')
        iterator = iter([1, 2])
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)

    def test_next_at_end(self):
        next = get_function('next')
        with self.assertRaises(StopIteration):
            next(iter([]))
        iterator = iter([1, 2])
        next(iterator)
        next(iterator)
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_next_does_not_exhaust_iterator(self):
        next = get_function('next')
        iterator = iter([1, 2, 3])
        self.assertEqual(next(iterator), 1)
        self.assertEqual(list(iterator), [2, 3])
        iterator = (n**2 for n in range(1000000000))
        self.assertEqual(next(iterator), 0)
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 4)
        self.assertEqual(next(iterator), 9)

    def test_next_with_default_value(self):
        next = get_function('next')
        iterator = iter([1, 2])
        self.assertEqual(next(iterator, 0), 1)
        self.assertEqual(next(iterator, 0), 2)
        self.assertEqual(next(iterator, 0), 0)
        self.assertEqual(next(iterator, 0), 0)
        self.assertIsNone(next(iterator, None))

    def test_next_on_non_iterator(self):
        next = get_function('next')
        with self.assertRaises(TypeError):
            next([1, 2])
        with self.assertRaises(TypeError):
            next({1, 2, 3})
        with self.assertRaises(TypeError):
            next(())
        with self.assertRaises(TypeError):
            next({'a': 1, 'b': 2})
        with self.assertRaises(TypeError):
            next('hello')


def get_function(name):
    """
    A magical function which imports the given name from my_builtins
    """
    sys.modules.pop('my_builtins', None)

    # Get source code
    spec = importlib.util.find_spec('my_builtins')
    source = spec.loader.get_source('my_builtins')

    # Make sure builtins module isn't imported in source
    if re.search(r"(import|from)\s*builtins", source):
        raise Exception("Can't import from builtins module")

    # Monkey patch and import
    my_builtins = importlib.util.module_from_spec(spec)
    code_obj = compile(source, my_builtins.__spec__.origin, 'exec')
    import builtins
    original = getattr(builtins, name)
    delattr(builtins, name)
    try:
        exec(code_obj, my_builtins.__dict__)
        sys.modules['my_builtins'] = my_builtins
    finally:
        setattr(builtins, name, original)

    # Return function from my_builtins module
    return getattr(my_builtins, name)


class BufferedStringIO(TextIOWrapper):

    def __init__(self, value='', **kwargs):
        super().__init__(BytesIO(value.encode('utf-8')), **kwargs)

    def getvalue(self):
        return self.buffer.getvalue().decode('utf-8').replace('\r\n', '\n')


if __name__ == "__main__":
    unittest.main(verbosity=2)
