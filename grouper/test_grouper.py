from operator import itemgetter
import unittest

from grouper import Grouper


class GrouperTests(unittest.TestCase):

    """Tests for Grouper."""

    def test_test_tuples_of_strings(self):
        animals = [
            ('agatha', 'dog'),
            ('kurt', 'cat'),
            ('margaret', 'mouse'),
            ('cory', 'cat'),
            ('mary', 'mouse'),
        ]
        animals_by_type = {
            'mouse': [('margaret', 'mouse'), ('mary', 'mouse')],
            'dog': [('agatha', 'dog')],
            'cat': [('kurt', 'cat'), ('cory', 'cat')],
        }
        groups = Grouper(animals, key=itemgetter(1))
        self.assertEqual(dict(groups), animals_by_type)

    def test_no_iterable_given(self):
        groups = Grouper(key=str.lower)
        self.assertEqual(dict(groups), {})

    def test_strings(self):
        words = ["Apple", "animal", "apple", "ANIMAL", "animal"]
        word_groups = {
            "apple": ["Apple", "apple"],
            "animal": ["animal", "ANIMAL", "animal"],
        }
        groups = Grouper(words, key=str.lower)
        self.assertEqual(dict(groups), word_groups)

    def test_containment(self):
        words = ["Apple", "animal", "apple", "ANIMAL", "animal"]
        groups = Grouper(words, key=str.lower)
        self.assertIn('apple', groups)

    def test_lookups(self):
        words = ["Apple", "animal", "apple", "ANIMAL", "animal"]
        groups = Grouper(words, key=str.lower)
        self.assertEqual(groups['apple'], ["Apple", "apple"])

    def test_init_accepts_mapping(self):
        dictionary = {
            "apple": ["Apple", "apple"],
            "lemon": ["lemon"],
        }
        groups = Grouper(dictionary, key=str.lower)
        self.assertEqual(dict(groups), dictionary)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_custom_update_method(self):
        words = ["Apple", "animal", "apple", "ANIMAL", "animal"]
        word_groups = {
            "apple": ["Apple", "apple", "APPLE", "APPLE"],
            "animal": ["animal", "ANIMAL", "animal"],
            "lemon": ["lemon", "Lemon", "lemon", "LEMON"],
            "orange": ["Orange"],
        }
        more_items = {
            "apple": ["APPLE"],
            "lemon": ["lemon", "LEMON"],
            "orange": ["Orange"],
        }
        groups = Grouper(words, key=str.lower)
        groups.update(["lemon", "Lemon", "APPLE"])
        groups.update(more_items)
        self.assertEqual(dict(groups), word_groups)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_add_and_group_for_methods(self):
        names = ["Trey Hunner", "Monica Marshall", "Katherine Hunner"]
        def last_name(name): return name.rsplit()[-1]
        name_groups = Grouper(names, key=last_name)
        self.assertEqual(name_groups.group_for("Rose Hunner"), "Hunner")
        self.assertEqual(name_groups.group_for("Rose Klyce"), "Klyce")
        self.assertEqual(
            name_groups['Hunner'],
            ["Trey Hunner", "Katherine Hunner"],
        )
        name_groups.add('Rose Hunner')
        self.assertEqual(
            name_groups['Hunner'],
            ["Trey Hunner", "Katherine Hunner", "Rose Hunner"],
        )
        name_groups.add("Rose Klyce")
        self.assertEqual(name_groups['Klyce'], ["Rose Klyce"])

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_adding_grouper_objects_together(self):
        words1 = ["apple", "animal", "lemon", "ANIMAL", "Apple"]
        words2 = ["Lemon", "Animal", "Apple", "lemon"]
        word_groups = {
            "apple": ["apple", "Apple", "Apple"],
            "animal": ["animal", "ANIMAL", "Animal"],
            "lemon": ["lemon", "Lemon", "lemon"],
        }
        groups1 = Grouper(words1, key=str.lower)
        groups2 = Grouper(words2, key=str.lower)
        self.assertEqual(dict(groups1 + groups2), word_groups)
        groups3 = Grouper(words2, key=str.upper)
        with self.assertRaises(ValueError):
            groups1 + groups3  # Can't concatenate groups with different keys


if __name__ == "__main__":
    unittest.main(verbosity=2)
