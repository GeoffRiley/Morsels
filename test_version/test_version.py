import unittest

from version import Version


class VersionTests(unittest.TestCase):
    def test_valid_versions(self):
        for ver, ver_rep in [('1.0.0', '1.0.0'), ('2.1', '2.1.0'),
                             ('3', '3.0.0')]:
            ver1 = Version(ver)
            self.assertEqual(str(ver1), ver_rep)

    def test_invalid_versions(self):
        for ver in ['', 'Version', '0.0.1.0', '1.0.0b', 'a.b.c']:
            with self.assertRaises(ValueError):
                _ = Version(ver)

    def test_string_representations(self):
        v1 = Version('1.2.3')
        self.assertEqual(str(v1), '1.2.3')
        self.assertEqual(repr(v1), "Version('1.2.3')")

    def test_instances_equal_values(self):
        v1 = Version('1.2.3')
        v2 = Version('1.2.3')
        v3 = Version('1.2.0')
        v4 = Version('1.2')
        self.assertTrue(v1 == v2)
        self.assertTrue(v1 != v3)
        self.assertTrue(v3 == v4)
        self.assertFalse(v1 != v2)
        self.assertFalse(v1 == v3)

    def test_version_comparisions(self):
        v1 = Version('1')
        v2 = Version('1.1')
        v3 = Version('2')
        v4 = Version('2.0.0')

        self.assertTrue(v1 < v2)
        self.assertTrue(v2 > v1)
        self.assertTrue(v1 <= v2)
        self.assertTrue(v2 >= v1)
        self.assertTrue(v3 <= v4)
        self.assertTrue(v3 >= v4)
        self.assertFalse(v1 > v2)
        self.assertFalse(v2 < v1)
        self.assertFalse(v1 >= v2)
        self.assertFalse(v2 <= v1)

    def test_less_than_not_version(self):
        v1 = Version('1')
        self.assertTrue(v1.__eq__('1') in [True, NotImplemented])
        self.assertTrue(v1.__ne__('1') in [False, NotImplemented])
        self.assertTrue(v1.__lt__('1.1') in [True, NotImplemented])
        self.assertTrue(v1.__gt__('1.1') in [False, NotImplemented])
        self.assertTrue(v1.__le__('1.1') in [True, NotImplemented])
        self.assertTrue(v1.__ge__('1.1') in [False, NotImplemented])


if __name__ == '__main__':
    unittest.main(verbosity=2)
