import unittest


from sortutils import natural_sort


class NaturalSortTests(unittest.TestCase):

    """Tests for natural_sort."""

    def test_empty_iterable(self):
        self.assertEqual(natural_sort([]), [])
        self.assertEqual(natural_sort(()), [])
        self.assertEqual(natural_sort(set()), [])

    def test_all_lowercase_strings(self):
        self.assertEqual(
            natural_sort(['cake', 'apple', 'ball', 'clover', 'zoo']),
            ['apple', 'ball', 'cake', 'clover', 'zoo'],
        )

    def test_some_uppercase(self):
        self.assertEqual(
            natural_sort(['Cake', 'apple', 'ball', 'clover', 'Zoo']),
            ['apple', 'ball', 'Cake', 'clover', 'Zoo'],
        )

    def test_with_spaces(self):
        self.assertEqual(
            natural_sort(['Sarah Clarke', 'Sara Hillard', 'Sarah Chiu']),
            ['Sara Hillard', 'Sarah Chiu', 'Sarah Clarke'],
        )

    def test_descending_sort(self):
        self.assertEqual(
            natural_sort(['Cake', 'apple', 'ball', 'clover', 'Zoo']),
            ['apple', 'ball', 'Cake', 'clover', 'Zoo'],
        )

    def test_reverse_order(self):
        self.assertEqual(
            natural_sort(
                ['Cake', 'apple', 'ball', 'clover', 'Zoo'],
                reverse=True,
            ),
            ['Zoo', 'clover', 'Cake', 'ball', 'apple']
        )
        self.assertEqual(
            natural_sort(
                ['Cake', 'apple', 'ball', 'clover', 'Zoo'],
                reverse=False,
            ),
            ['apple', 'ball', 'Cake', 'clover', 'Zoo']
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_natural_key_function_and_key_argument(self):
        from sortutils import natural_key
        self.assertEqual(
            natural_sort(['cake', 'Zoo', 'Cake', 'zoo'], key=natural_key),
            ['cake', 'Cake', 'Zoo', 'zoo'],
        )
        names = ['Sarah Clarke', 'Sara Hillard', 'Sarah Chiu']
        self.assertEqual(
            natural_sort(names, key=lambda s: natural_sort(' '.join(s.split()[::-1]))),
            ['Sarah Chiu', 'Sarah Clarke', 'Sara Hillard'],
        )
        # Make sure sort is stable
        self.assertEqual(
            natural_sort(['cake', 'Zoo', 'Cake', 'ball', 'cakE', 'zoo']),
            ['ball', 'cake', 'Cake', 'cakE', 'Zoo', 'zoo'],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_sorting_with_numbers(self):
        self.assertEqual(
            natural_sort(['take 8', 'take 11', 'take 9', 'take 10', 'take 1']),
            ['take 1', 'take 8', 'take 9', 'take 10', 'take 11'],
        )
        self.assertEqual(
            natural_sort(['02', '1', '16', '17', '20', '26', '3', '30']),
            ['1', '02', '3', '16', '17', '20', '26', '30'],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_allow_registering_different_types(self):
        from sortutils import natural_key
        @natural_key.register(tuple)
        def sort_each(items):
            return [natural_key(x) for x in items]
        name_tuples = [('Chiu', 'Sarah'), ('Bailey', 'Lou'), ('Chiu', 'Alice')]
        self.assertEqual(
            natural_sort(name_tuples),
            [('Bailey', 'Lou'), ('Chiu', 'Alice'), ('Chiu', 'Sarah')],
        )
        from pathlib import Path
        @natural_key.register(Path)
        def path_parts(path):
            return natural_key(path.parts)  # Relies on tuple sorting above
        self.assertEqual(
            natural_sort([Path('docs (old)/file1'), Path('docs/file1')]),
            [Path('docs/file1'), Path('docs (old)/file1')],
        )
        @natural_key.register(Path)  # We're redefining how Path sorting works
        def path_to_string(path):
            return str(path)
        name_tuples = [('Chiu', 'Sarah'), ('Bailey', 'Lou'), ('Chiu', 'Alice')]
        self.assertEqual(
            natural_sort([Path('docs (old)/file1'), Path('docs/file1')]),
            [Path('docs (old)/file1'), Path('docs/file1')],
        )
        with self.assertRaises(TypeError):
            natural_sort([object(), object()])


if __name__ == "__main__":
    unittest.main(verbosity=2)
