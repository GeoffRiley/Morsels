import unittest

import easyjson


class ParseTests(unittest.TestCase):
    """Tests for parse."""
    def test_dictionary_key_syntax(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "is active": true,
            "numbers": [1, 2, 3]
        }""")
        self.assertEqual(data['user'], "Trey")
        self.assertIs(data['is active'], True)
        self.assertEqual(data['numbers'], [1, 2, 3])

    def test_attribute_syntax(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "is_active": true,
            "numbers": [1, 2, 3]
        }""")
        self.assertEqual(data.user, "Trey")
        self.assertEqual(data.numbers, [1, 2, 3])

    def test_deep_objects(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "colors": {
                "red": true,
                "green": false,
                "blue": true
            }
        }""")
        self.assertIs(data.colors.red, True)
        self.assertIs(data.colors.green, False)
        self.assertIs(data.colors.blue, True)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_repr_equality_and_dict_conversion(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "numbers": [1, 2, 3],
            "colors": {
                "red": true,
                "green": false,
                "blue": true
            }
        }""")
        self.assertEqual(
            data.colors,
            {
                'red': True,
                'green': False,
                'blue': True
            },
        )
        self.assertEqual(eval(repr(data)), data)
        self.assertEqual(
            dict(data.colors),
            {
                'red': True,
                'green': False,
                'blue': True
            },
        )
        self.assertEqual(set({**data}), {"user", "numbers", "colors"})

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_tuples_as_keys(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "numbers": [1, 2, 3],
            "colors": {
                "red": true,
                "green": false,
                "blue": true
            }
        }""")
        self.assertEqual(
            data['user', 'numbers'],
            {
                'user': 'Trey',
                'numbers': [1, 2, 3]
            },
        )
        self.assertEqual(data['user', 'colors'].colors.red, True)
        self.assertEqual(
            data.colors['red', 'blue'],
            {
                'red': True,
                'blue': True
            },
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_querying_arrays(self):
        # Querying objects in an array
        data = easyjson.parse("""[{
            "id": 1,
            "user": "Robert"
        }, {
            "id": 2,
            "user": "Cheryl"
        }, {
            "id": 3,
            "user": "Linda"
        }]""")
        self.assertEqual(list(data[...]['id']), [1, 2, 3])
        self.assertEqual(list(data[...].user), ["Robert", "Cheryl", "Linda"])

        # Querying array of arrays
        data = easyjson.parse("""[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]""")
        self.assertEqual(list(data[...][0]), [1, 4, 7])
        self.assertEqual(list(data[...][2]), [3, 6, 9])

        # Only queries one level deep
        data = easyjson.parse("""{
            "result": {
                "users": [{
                    "id": 4,
                    "profile": {"id": 16, "name": "Mildred"}
                }, {
                    "id": 6,
                    "profile": {"id": 18, "name": "James"}
                }, {
                    "id": 5,
                    "profile": {"id": 17, "name": "Gloria"}
                }, {
                    "id": 3,
                    "profile": {"id": 15, "name": "William"}
                }]
            }
        }""")
        users = data.result.users
        self.assertEqual(list(users[...].id), [4, 6, 5, 3])
        self.assertEqual(users[...].profile[2], {"id": 17, "name": "Gloria"})
        self.assertEqual(users[...].profile[0]['name'], "Mildred")
        self.assertEqual(users[...].profile[1].id, 18)
        self.assertEqual(list(users[...].profile[...].id), [16, 18, 17, 15])


if __name__ == "__main__":
    unittest.main(verbosity=2)
