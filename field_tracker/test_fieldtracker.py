import unittest

from fieldtracker import FieldTracker


class Point(FieldTracker):
    fields = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.saved = 0
        super().__init__()

    def save(self):
        self.saved += 1
        super().save()


class FieldTrackerTests(unittest.TestCase):
    """Tests for FieldTracker."""
    def test_initialization(self):
        class Point(FieldTracker):
            fields = ('x', 'y', 'z')

            def __init__(self, x, y, z):
                self.x, self.y, self.z = x, y, z
                super().__init__()

        p = Point(1, 2, 3)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.z, 3)

    def test_save_method(self):
        class Point(FieldTracker):
            fields = ('x', 'y', 'z')

            def __init__(self, x, y, z):
                self.x, self.y, self.z = x, y, z
                self.saved = 0
                super().__init__()

            def save(self):
                self.saved += 1
                super().save()

        p = Point(1, 2, 3)
        self.assertEqual(p.saved, 0)
        p.save()
        self.assertEqual(p.saved, 1)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.z, 3)
        p.save()
        self.assertEqual(p.saved, 2)

    def test_changed_method(self):
        p = Point(1, 2, 3)
        self.assertEqual(p.changed(), {})
        p.x = 4
        self.assertEqual(p.changed(), {'x': 1})
        self.assertEqual(p.x, 4)
        p.z = 6
        self.assertEqual(p.changed(), {'x': 1, 'z': 3})
        p.save()
        self.assertEqual(p.changed(), {})
        p.y = 8
        self.assertEqual(p.changed(), {'y': 2})
        self.assertEqual(p.y, 8)
        p.save()
        self.assertEqual(p.changed(), {})
        p.save()
        self.assertEqual(p.changed(), {})

    def test_has_changed(self):
        p = Point(1, 2, 3)
        self.assertFalse(p.has_changed('x'))
        self.assertFalse(p.has_changed('y'))
        self.assertFalse(p.has_changed('z'))
        p.x = 4
        self.assertTrue(p.has_changed('x'))
        self.assertFalse(p.has_changed('y'))
        self.assertFalse(p.has_changed('z'))
        p.z = 6
        self.assertTrue(p.has_changed('x'))
        self.assertFalse(p.has_changed('y'))
        self.assertTrue(p.has_changed('z'))
        p.save()
        self.assertFalse(p.has_changed('x'))
        self.assertFalse(p.has_changed('y'))
        self.assertFalse(p.has_changed('z'))
        p.y = 8
        self.assertFalse(p.has_changed('x'))
        self.assertTrue(p.has_changed('y'))
        self.assertFalse(p.has_changed('z'))
        p.save()
        self.assertFalse(p.has_changed('x'))
        self.assertFalse(p.has_changed('y'))
        self.assertFalse(p.has_changed('z'))

    def test_previous_method(self):
        p = Point(1, 2, 3)
        self.assertEqual(p.previous('x'), 1)
        p.x = 4
        self.assertEqual(p.previous('x'), 1)
        self.assertEqual(p.x, 4)
        p.z = 6
        self.assertEqual(p.previous('x'), 1)
        self.assertEqual(p.previous('y'), 2)
        self.assertEqual(p.previous('z'), 3)
        p.save()
        self.assertEqual(p.previous('x'), 4)
        self.assertEqual(p.previous('y'), 2)
        self.assertEqual(p.previous('z'), 6)
        p.y = 8
        self.assertEqual(p.previous('y'), 2)
        self.assertEqual(p.y, 8)
        p.save()
        self.assertEqual(p.previous('y'), 8)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_mixin(self):
        from fieldtracker import FieldTrackerMixin

        class DBModel:
            def __init__(self, **kwargs):
                self.id = None
                for name, value in kwargs.items():
                    setattr(self, name, value)

            def save(self):
                self.id = 4  # This would be auto-generated normally
                self.stored = True  # Pretending to put stuff in a database

        class Person(FieldTrackerMixin, DBModel):
            fields = ('id', 'name', 'email')

        trey = Person(name="Trey", email="trey@trey.com")
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.email, "trey@trey.com")
        self.assertIsNone(trey.id)
        self.assertEqual(trey.changed(), {})
        self.assertFalse(trey.has_changed('email'))
        self.assertEqual(trey.previous('email'), "trey@trey.com")
        trey.email = "trey@gmail.com"
        self.assertEqual(trey.previous('email'), "trey@trey.com")
        self.assertTrue(trey.has_changed('email'))
        self.assertEqual(trey.changed(), {'email': "trey@trey.com"})
        trey.save()
        self.assertEqual(trey.changed(), {})
        self.assertFalse(trey.has_changed('email'))
        self.assertEqual(trey.previous('email'), "trey@gmail.com")
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.email, "trey@gmail.com")
        self.assertEqual(trey.id, 4)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_raise_friendly_errors(self):
        # ValueError raised for invalid fields
        p = Point(1, 2, 3)
        with self.assertRaises(ValueError):
            p.has_changed('w')
        with self.assertRaises(ValueError):
            p.previous('w')

        # TypeError raised if no fields attribute specified
        class Vector(FieldTracker):
            # No fields!
            def __init__(self, x, y, z):
                self.x, self.y, self.z = x, y, z
                super().__init__()

        with self.assertRaises(TypeError):
            Vector(1, 2, 3)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_init_tracking_method(self):
        from fieldtracker import FieldTrackerMixin
        from dataclasses import dataclass

        class DBModel:
            def store(self):
                self.id = 4  # This would be auto-generated normally

        @dataclass
        class Person(FieldTrackerMixin, DBModel):
            fields = ('id', 'name', 'email')

            name: str
            email: str
            id: int = None

            def __post_init__(self):
                self.init_tracking()

            def store(self):
                self.id = 8
                self.set_saved_fields()

        trey = Person(name="Trey", email="trey@trey.com")
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.email, "trey@trey.com")
        self.assertIsNone(trey.id)
        self.assertEqual(trey.changed(), {})
        self.assertFalse(trey.has_changed('email'))
        self.assertEqual(trey.previous('email'), "trey@trey.com")
        trey.email = "trey@gmail.com"
        self.assertEqual(trey.previous('email'), "trey@trey.com")
        self.assertTrue(trey.has_changed('email'))
        self.assertEqual(trey.changed(), {'email': "trey@trey.com"})
        trey.store()
        self.assertEqual(trey.changed(), {})
        self.assertFalse(trey.has_changed('email'))
        self.assertEqual(trey.previous('email'), "trey@gmail.com")
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.email, "trey@gmail.com")
        self.assertEqual(trey.id, 8)


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    import sys
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
