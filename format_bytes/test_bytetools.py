import unittest


from bytetools import format_bytes


class FormatBytesTests(unittest.TestCase):

    """Tests for format_bytes."""

    def test_bytes(self):
        self.assertEqual(format_bytes(0), '0B')
        self.assertEqual(format_bytes(95), '95B')

    def test_kilobytes(self):
        self.assertEqual(format_bytes(1000), '1KB')
        self.assertEqual(format_bytes(15000), '15KB')
        self.assertEqual(format_bytes(12345), '12KB')

    def test_megabytes(self):
        self.assertEqual(format_bytes(1000000), '1MB')
        self.assertEqual(format_bytes(9800004), '10MB')
        self.assertEqual(format_bytes(98000040), '98MB')
        self.assertEqual(format_bytes(123456789), '123MB')

    def test_gigabytes(self):
        self.assertEqual(format_bytes(1234567890), '1GB')
        self.assertEqual(format_bytes(75000000020), '75GB')

    def test_terabytes(self):
        self.assertEqual(format_bytes(7500000002000), '8TB')

    def test_error_for_negative_bytes(self):
        with self.assertRaises(ValueError):
            format_bytes(-100)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_bits(self):
        self.assertEqual(format_bytes(0, bits=True), '0b')
        self.assertEqual(format_bytes(1000000, bits=True), '8Mb')
        self.assertEqual(format_bytes(1, bits=True), '8b')
        self.assertEqual(format_bytes(500, bits=True), '4Kb')
        self.assertEqual(format_bytes(7000, bits=True), '56Kb')
        self.assertEqual(format_bytes(37500000, bits=True), '300Mb')
        self.assertEqual(format_bytes(123000000, bits=True), '984Mb')
        self.assertEqual(format_bytes(123456789, bits=True), '988Mb')
        self.assertEqual(format_bytes(123456789, bits=False), '123MB')

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_base_2(self):
        self.assertEqual(format_bytes(1000000, binary=True), '977KiB')
        self.assertEqual(format_bytes(7000, binary=True), '7KiB')
        self.assertEqual(format_bytes(37500000, binary=True), '36MiB')
        self.assertEqual(format_bytes(1000000000000, binary=True), '931GiB')
        self.assertEqual(format_bytes(2000000000000, binary=True), '2TiB')
        self.assertEqual(format_bytes(123000000, binary=True), '117MiB')
        self.assertEqual(format_bytes(123456789, binary=True), '118MiB')
        self.assertEqual(format_bytes(1, binary=True), '1B')
        self.assertEqual(format_bytes(37500000, binary=False), '38MB')


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class ParseBytesTests(unittest.TestCase):

    """Tests for parse_bytes."""

    def test_bytes(self):
        from bytetools import parse_bytes
        self.assertEqual(parse_bytes('0B'), 0)
        self.assertEqual(parse_bytes('95B'), 95)

    def test_kilobytes(self):
        from bytetools import parse_bytes
        self.assertEqual(parse_bytes('1KB'), 1000)
        self.assertEqual(parse_bytes('15KB'), 15000)
        self.assertEqual(parse_bytes('12KB'), 12000)

    def test_megabytes(self):
        from bytetools import parse_bytes
        self.assertEqual(parse_bytes('1MB'), 1000000)
        self.assertEqual(parse_bytes('10MB'), 10000000)
        self.assertEqual(parse_bytes('98MB'), 98000000)
        self.assertEqual(parse_bytes('123MB'), 123000000)

    def test_gigabytes(self):
        from bytetools import parse_bytes
        self.assertEqual(parse_bytes('1GB'), 1000000000)
        self.assertEqual(parse_bytes('75GB'), 75000000000)

    def test_terabytes(self):
        from bytetools import parse_bytes
        self.assertEqual(parse_bytes('8TB'), 8000000000000)

    def test_bits(self):
        from bytetools import parse_bytes
        self.assertEqual(parse_bytes('8Mb'), 1000000)
        self.assertEqual(parse_bytes('8b'), 1)
        self.assertEqual(parse_bytes('56Kb'), 7000)
        self.assertEqual(parse_bytes('300Mb'), 37500000)
        self.assertEqual(parse_bytes('984Mb'), 123000000)
        self.assertEqual(parse_bytes('988Mb'), 123500000)

    def test_binary_suffixes(self):
        from bytetools import parse_bytes
        self.assertEqual(parse_bytes('977KiB'), 1000448)
        self.assertEqual(parse_bytes('7KiB'), 7168)
        self.assertEqual(parse_bytes('36MiB'), 37748736)
        self.assertEqual(parse_bytes('931GiB'), 999653638144)
        self.assertEqual(parse_bytes('2TiB'), 2199023255552)
        self.assertEqual(parse_bytes('117MiB'), 122683392)
        self.assertEqual(parse_bytes('118MiB'), 123731968)
        self.assertEqual(parse_bytes('1B'), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
