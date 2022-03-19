from contextlib import contextmanager
from datetime import datetime
from ipaddress import IPv4Address
import os
from tempfile import NamedTemporaryFile
import unittest
import gzip

from log_parser import get_user_logins


class GetUserLoginsTests(unittest.TestCase):
    """Tests for get_user_logins"""
    def test_no_user_logins(self):
        with make_gz_file(no_sessions) as gz_file:
            self.assertEqual(list(get_user_logins(gz_file)), [])

    def test_one_user_login(self):
        with make_gz_file(one_session) as gz_file:
            self.assertEqual(list(get_user_logins(gz_file)), ['nancy'])

    def test_two_different_users(self):
        with make_gz_file(two_sessions) as gz_file:
            self.assertEqual(
                set(get_user_logins(gz_file)),
                {'nancy', 'taylor'},
            )

    def test_same_user_multiple_times(self):
        with make_gz_file(eight_sessions) as gz_file:
            self.assertEqual(
                set(get_user_logins(gz_file)),
                {'nancy', 'taylor', 'virgil'},
            )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class GetFailedLoginsTests(unittest.TestCase):
    """Tests for get_failed_logins"""

    maxDiff = 5000

    def test_three_failed_from_one_ip(self):
        from log_parser import get_failed_logins
        with make_gz_file(one_session) as gz_file:
            self.assertEqual(
                get_failed_logins(gz_file),
                {'218.65.30.126': ['root', 'root', 'root']},
            )

    def test_many_attempts_from_one_ip(self):
        from log_parser import get_failed_logins
        with make_gz_file(no_sessions) as gz_file:
            self.assertEqual(
                get_failed_logins(gz_file),
                {'116.31.116.15': ['root'] * 50},
            )

    def test_two_ips(self):
        from log_parser import get_failed_logins
        with make_gz_file(eight_sessions) as gz_file:
            self.assertEqual(
                get_failed_logins(gz_file),
                {
                    '218.65.30.126': ['root'] * 35,
                    '112.217.49.149': ['student'],
                },
            )

    def test_three_ips(self):
        from log_parser import get_failed_logins
        with make_gz_file(three_failed) as gz_file:
            self.assertEqual(
                get_failed_logins(gz_file),
                {
                    '112.217.49.149': ['pi'],
                    '181.211.138.186': ['admin'] * 6,
                    '116.31.116.15': ['root'] * 12,
                },
            )


class BaseGetSessionsTests(unittest.TestCase):

    maxDiff = 5000

    def assertSessionsEqualish(self,
                               actual_sessions,
                               expected_sessions,
                               full=False):
        actual_sessions = list(actual_sessions)
        self.assertEqual(
            len(actual_sessions),
            len(expected_sessions),
            f"Expected {len(expected_sessions)} sessions",
        )
        for actual, expected in zip(actual_sessions, expected_sessions):
            self.assertEqual(
                (actual.pid, actual.user, actual.opened),
                (expected.pid, expected.user, expected.opened),
            )
            if full:
                self.assertEqual(
                    (actual.pid, actual.closed, actual.ip),
                    (expected.pid, expected.closed, expected.ip),
                )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class GetSessionsTests(BaseGetSessionsTests):
    """Tests for get_sessions"""

    maxDiff = 5000

    def assertSessionsEqualish(self,
                               actual_sessions,
                               expected_sessions,
                               full=False):
        actual_sessions = list(actual_sessions)
        self.assertEqual(
            len(actual_sessions),
            len(expected_sessions),
            f"Expected {len(expected_sessions)} sessions",
        )
        for actual, expected in zip(actual_sessions, expected_sessions):
            self.assertEqual(
                (actual.pid, actual.user, actual.opened),
                (expected.pid, expected.user, expected.opened),
            )
            if full:
                self.assertEqual(
                    (actual.pid, actual.closed, actual.ip),
                    (expected.pid, expected.closed, expected.ip),
                )

    def test_no_sessions(self):
        from log_parser import get_sessions
        with make_gz_file(no_sessions) as gz_file:
            self.assertSessionsEqualish(get_sessions(gz_file), [])

    def test_one_session_not_closed(self):
        from log_parser import get_sessions, Session
        with make_gz_file(one_session) as gz_file:
            opened = datetime(2017, 6, 4, 22, 4, 34)
            self.assertSessionsEqualish(get_sessions(gz_file, year=2017), [
                Session(pid=9804, user='nancy', opened=opened),
            ])

    def test_two_different_users(self):
        from log_parser import get_sessions, Session
        with make_gz_file(two_sessions) as gz_file:
            self.assertSessionsEqualish(
                get_sessions(gz_file),
                [
                    Session(
                        pid=9804,
                        user='nancy',
                        opened=datetime(2017, 6, 4, 22, 4, 34),
                    ),
                    Session(
                        pid=9907,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 7),
                    ),
                ],
            )

    def test_same_user_multiple_times(self):
        from log_parser import get_sessions, Session
        with make_gz_file(eight_sessions) as gz_file:
            self.assertSessionsEqualish(
                get_sessions(gz_file),
                [
                    Session(
                        pid=9804,
                        user='nancy',
                        opened=datetime(2017, 6, 4, 22, 4, 34),
                    ),
                    Session(
                        pid=9907,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 7),
                    ),
                    Session(
                        pid=9919,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 14),
                    ),
                    Session(
                        pid=9941,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 19),
                    ),
                    Session(
                        pid=9948,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 20),
                    ),
                    Session(
                        pid=9953,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 21),
                    ),
                    Session(
                        pid=9959,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 22),
                    ),
                    Session(
                        pid=9970,
                        user='virgil',
                        opened=datetime(2017, 6, 4, 22, 7, 33),
                    ),
                ],
            )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class MoreGetSessionsTests(BaseGetSessionsTests):
    """More tests for get_sessions"""

    maxDiff = 5000

    def test_with_ip_and_closed(self):
        from log_parser import get_sessions, Session
        with make_gz_file(eight_sessions) as gz_file:
            self.assertSessionsEqualish(
                get_sessions(gz_file),
                [
                    Session(
                        pid=9804,
                        user='nancy',
                        opened=datetime(2017, 6, 4, 22, 4, 34),
                        closed=None,
                        ip=IPv4Address('192.168.0.110'),
                    ),
                    Session(
                        pid=9907,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 7),
                        closed=datetime(2017, 6, 4, 22, 7, 7),
                        ip=IPv4Address('192.168.0.113'),
                    ),
                    Session(
                        pid=9919,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 14),
                        closed=datetime(2017, 6, 4, 22, 7, 16),
                        ip=IPv4Address('192.168.0.113'),
                    ),
                    Session(
                        pid=9941,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 19),
                        closed=datetime(2017, 6, 4, 22, 7, 19),
                        ip=IPv4Address('192.168.0.113'),
                    ),
                    Session(
                        pid=9948,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 20),
                        closed=datetime(2017, 6, 4, 22, 7, 20),
                        ip=IPv4Address('192.168.0.113'),
                    ),
                    Session(
                        pid=9953,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 21),
                        closed=datetime(2017, 6, 4, 22, 7, 21),
                        ip=IPv4Address('192.168.0.113'),
                    ),
                    Session(
                        pid=9959,
                        user='taylor',
                        opened=datetime(2017, 6, 4, 22, 7, 22),
                        closed=datetime(2017, 6, 4, 22, 7, 22),
                        ip=IPv4Address('192.168.0.113'),
                    ),
                    Session(
                        pid=9970,
                        user='virgil',
                        opened=datetime(2017, 6, 4, 22, 7, 33),
                        closed=None,
                        ip=IPv4Address('192.168.0.113'),
                    ),
                ],
                full=True,
            )


@contextmanager
def make_gz_file(contents):
    """Context manager providing name of a file containing given contents."""
    with NamedTemporaryFile(mode='wb', delete=False) as tmp_file:
        with gzip.GzipFile(fileobj=tmp_file, mode="w") as gzip_file:
            gzip_file.write(contents.encode('utf-8'))
    try:
        yield tmp_file.name
    finally:
        os.remove(tmp_file.name)


no_sessions = """
Jun 03 21:21:14 farnsworth sshd[28575]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:21:14 farnsworth sshd[28575]: input_userauth_request: invalid user root [preauth]
Jun 03 21:21:15 farnsworth sshd[28575]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:21:15 farnsworth sshd[28575]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:21:16 farnsworth sshd[28575]: Failed password for invalid user root from 116.31.116.15 port 43401 ssh2
Jun 03 21:21:16 farnsworth sshd[28575]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:21:18 farnsworth sshd[28575]: Failed password for invalid user root from 116.31.116.15 port 43401 ssh2
Jun 03 21:21:18 farnsworth sshd[28575]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:21:20 farnsworth sshd[28575]: Failed password for invalid user root from 116.31.116.15 port 43401 ssh2
Jun 03 21:21:20 farnsworth sshd[28575]: Received disconnect from 116.31.116.15 port 43401:11:  [preauth]
Jun 03 21:21:20 farnsworth sshd[28575]: Disconnected from 116.31.116.15 port 43401 [preauth]
Jun 03 21:21:20 farnsworth sshd[28575]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:22:00 farnsworth sshd[28580]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:22:00 farnsworth sshd[28580]: input_userauth_request: invalid user root [preauth]
Jun 03 21:22:00 farnsworth sshd[28580]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:22:00 farnsworth sshd[28580]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:22:01 farnsworth sshd[28580]: Failed password for invalid user root from 116.31.116.15 port 39679 ssh2
Jun 03 21:22:02 farnsworth sshd[28580]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:22:04 farnsworth sshd[28580]: Failed password for invalid user root from 116.31.116.15 port 39679 ssh2
Jun 03 21:22:04 farnsworth sshd[28580]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:22:06 farnsworth sshd[28580]: Failed password for invalid user root from 116.31.116.15 port 39679 ssh2
Jun 03 21:22:06 farnsworth sshd[28580]: Received disconnect from 116.31.116.15 port 39679:11:  [preauth]
Jun 03 21:22:06 farnsworth sshd[28580]: Disconnected from 116.31.116.15 port 39679 [preauth]
Jun 03 21:22:06 farnsworth sshd[28580]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:22:45 farnsworth sshd[28590]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:22:45 farnsworth sshd[28590]: input_userauth_request: invalid user root [preauth]
Jun 03 21:22:45 farnsworth sshd[28590]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:22:45 farnsworth sshd[28590]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:22:46 farnsworth sshd[28590]: Failed password for invalid user root from 116.31.116.15 port 28737 ssh2
Jun 03 21:22:47 farnsworth sshd[28590]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:22:49 farnsworth sshd[28590]: Failed password for invalid user root from 116.31.116.15 port 28737 ssh2
Jun 03 21:22:49 farnsworth sshd[28590]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:22:51 farnsworth sshd[28590]: Failed password for invalid user root from 116.31.116.15 port 28737 ssh2
Jun 03 21:22:51 farnsworth sshd[28590]: Received disconnect from 116.31.116.15 port 28737:11:  [preauth]
Jun 03 21:22:51 farnsworth sshd[28590]: Disconnected from 116.31.116.15 port 28737 [preauth]
Jun 03 21:22:51 farnsworth sshd[28590]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:23:29 farnsworth sshd[28594]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:23:29 farnsworth sshd[28594]: input_userauth_request: invalid user root [preauth]
Jun 03 21:23:29 farnsworth sshd[28594]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:23:29 farnsworth sshd[28594]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:23:31 farnsworth sshd[28594]: Failed password for invalid user root from 116.31.116.15 port 64860 ssh2
Jun 03 21:23:31 farnsworth sshd[28594]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:23:34 farnsworth sshd[28594]: Failed password for invalid user root from 116.31.116.15 port 64860 ssh2
Jun 03 21:23:34 farnsworth sshd[28594]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:23:36 farnsworth sshd[28594]: Failed password for invalid user root from 116.31.116.15 port 64860 ssh2
Jun 03 21:23:36 farnsworth sshd[28594]: Received disconnect from 116.31.116.15 port 64860:11:  [preauth]
Jun 03 21:23:36 farnsworth sshd[28594]: Disconnected from 116.31.116.15 port 64860 [preauth]
Jun 03 21:23:36 farnsworth sshd[28594]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:24:13 farnsworth sshd[28598]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:24:13 farnsworth sshd[28598]: input_userauth_request: invalid user root [preauth]
Jun 03 21:24:14 farnsworth sshd[28598]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:24:14 farnsworth sshd[28598]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:24:15 farnsworth sshd[28598]: Failed password for invalid user root from 116.31.116.15 port 43122 ssh2
Jun 03 21:24:15 farnsworth sshd[28598]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:24:17 farnsworth sshd[28598]: Failed password for invalid user root from 116.31.116.15 port 43122 ssh2
Jun 03 21:24:17 farnsworth sshd[28598]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:24:19 farnsworth sshd[28598]: Failed password for invalid user root from 116.31.116.15 port 43122 ssh2
Jun 03 21:24:19 farnsworth sshd[28598]: Received disconnect from 116.31.116.15 port 43122:11:  [preauth]
Jun 03 21:24:19 farnsworth sshd[28598]: Disconnected from 116.31.116.15 port 43122 [preauth]
Jun 03 21:24:19 farnsworth sshd[28598]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:25:00 farnsworth sshd[28606]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:25:00 farnsworth sshd[28606]: input_userauth_request: invalid user root [preauth]
Jun 03 21:25:00 farnsworth sshd[28606]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:25:00 farnsworth sshd[28606]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:25:02 farnsworth sshd[28606]: Failed password for invalid user root from 116.31.116.15 port 41178 ssh2
Jun 03 21:25:02 farnsworth sshd[28606]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:25:04 farnsworth sshd[28606]: Failed password for invalid user root from 116.31.116.15 port 41178 ssh2
Jun 03 21:25:04 farnsworth sshd[28606]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:25:06 farnsworth sshd[28606]: Failed password for invalid user root from 116.31.116.15 port 41178 ssh2
Jun 03 21:25:06 farnsworth sshd[28606]: Received disconnect from 116.31.116.15 port 41178:11:  [preauth]
Jun 03 21:25:06 farnsworth sshd[28606]: Disconnected from 116.31.116.15 port 41178 [preauth]
Jun 03 21:25:06 farnsworth sshd[28606]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:25:46 farnsworth sshd[28612]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:25:46 farnsworth sshd[28612]: input_userauth_request: invalid user root [preauth]
Jun 03 21:25:47 farnsworth sshd[28612]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:25:47 farnsworth sshd[28612]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:25:48 farnsworth sshd[28612]: Failed password for invalid user root from 116.31.116.15 port 48174 ssh2
Jun 03 21:25:49 farnsworth sshd[28612]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:25:51 farnsworth sshd[28612]: Failed password for invalid user root from 116.31.116.15 port 48174 ssh2
Jun 03 21:25:51 farnsworth sshd[28612]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:25:54 farnsworth sshd[28612]: Failed password for invalid user root from 116.31.116.15 port 48174 ssh2
Jun 03 21:25:54 farnsworth sshd[28612]: Received disconnect from 116.31.116.15 port 48174:11:  [preauth]
Jun 03 21:25:54 farnsworth sshd[28612]: Disconnected from 116.31.116.15 port 48174 [preauth]
Jun 03 21:25:54 farnsworth sshd[28612]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:26:31 farnsworth sshd[28616]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:26:31 farnsworth sshd[28616]: input_userauth_request: invalid user root [preauth]
Jun 03 21:26:31 farnsworth sshd[28616]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:26:31 farnsworth sshd[28616]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:26:32 farnsworth sshd[28616]: Failed password for invalid user root from 116.31.116.15 port 31132 ssh2
Jun 03 21:26:33 farnsworth sshd[28616]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:26:35 farnsworth sshd[28616]: Failed password for invalid user root from 116.31.116.15 port 31132 ssh2
Jun 03 21:26:35 farnsworth sshd[28616]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:26:37 farnsworth sshd[28616]: Failed password for invalid user root from 116.31.116.15 port 31132 ssh2
Jun 03 21:26:37 farnsworth sshd[28616]: Received disconnect from 116.31.116.15 port 31132:11:  [preauth]
Jun 03 21:26:37 farnsworth sshd[28616]: Disconnected from 116.31.116.15 port 31132 [preauth]
Jun 03 21:26:37 farnsworth sshd[28616]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:27:17 farnsworth sshd[28622]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:27:17 farnsworth sshd[28622]: input_userauth_request: invalid user root [preauth]
Jun 03 21:27:17 farnsworth sshd[28622]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:27:17 farnsworth sshd[28622]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:27:18 farnsworth sshd[28622]: Failed password for invalid user root from 116.31.116.15 port 49856 ssh2
Jun 03 21:27:19 farnsworth sshd[28622]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:27:21 farnsworth sshd[28622]: Failed password for invalid user root from 116.31.116.15 port 49856 ssh2
Jun 03 21:27:21 farnsworth sshd[28622]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:27:23 farnsworth sshd[28622]: Failed password for invalid user root from 116.31.116.15 port 49856 ssh2
Jun 03 21:27:23 farnsworth sshd[28622]: Received disconnect from 116.31.116.15 port 49856:11:  [preauth]
Jun 03 21:27:23 farnsworth sshd[28622]: Disconnected from 116.31.116.15 port 49856 [preauth]
Jun 03 21:27:23 farnsworth sshd[28622]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:28:01 farnsworth sshd[28633]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:28:01 farnsworth sshd[28633]: input_userauth_request: invalid user root [preauth]
Jun 03 21:28:01 farnsworth sshd[28633]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:28:01 farnsworth sshd[28633]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:28:02 farnsworth sshd[28633]: Failed password for invalid user root from 116.31.116.15 port 26480 ssh2
Jun 03 21:28:03 farnsworth sshd[28633]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:28:04 farnsworth sshd[28633]: Failed password for invalid user root from 116.31.116.15 port 26480 ssh2
Jun 03 21:28:05 farnsworth sshd[28633]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:28:07 farnsworth sshd[28633]: Failed password for invalid user root from 116.31.116.15 port 26480 ssh2
Jun 03 21:28:07 farnsworth sshd[28633]: Received disconnect from 116.31.116.15 port 26480:11:  [preauth]
Jun 03 21:28:07 farnsworth sshd[28633]: Disconnected from 116.31.116.15 port 26480 [preauth]
Jun 03 21:28:07 farnsworth sshd[28633]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:28:46 farnsworth sshd[28636]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:28:46 farnsworth sshd[28636]: input_userauth_request: invalid user root [preauth]
Jun 03 21:28:46 farnsworth sshd[28636]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:28:46 farnsworth sshd[28636]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:28:48 farnsworth sshd[28636]: Failed password for invalid user root from 116.31.116.15 port 25694 ssh2
Jun 03 21:28:49 farnsworth sshd[28636]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:28:50 farnsworth sshd[28636]: Failed password for invalid user root from 116.31.116.15 port 25694 ssh2
Jun 03 21:28:50 farnsworth sshd[28636]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:28:52 farnsworth sshd[28636]: Failed password for invalid user root from 116.31.116.15 port 25694 ssh2
Jun 03 21:28:52 farnsworth sshd[28636]: Received disconnect from 116.31.116.15 port 25694:11:  [preauth]
Jun 03 21:28:52 farnsworth sshd[28636]: Disconnected from 116.31.116.15 port 25694 [preauth]
Jun 03 21:28:52 farnsworth sshd[28636]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:29:30 farnsworth sshd[28642]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:29:30 farnsworth sshd[28642]: input_userauth_request: invalid user root [preauth]
Jun 03 21:29:30 farnsworth sshd[28642]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:29:30 farnsworth sshd[28642]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:29:33 farnsworth sshd[28642]: Failed password for invalid user root from 116.31.116.15 port 57447 ssh2
Jun 03 21:29:33 farnsworth sshd[28642]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:29:35 farnsworth sshd[28642]: Failed password for invalid user root from 116.31.116.15 port 57447 ssh2
Jun 03 21:29:36 farnsworth sshd[28642]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:29:38 farnsworth sshd[28642]: Failed password for invalid user root from 116.31.116.15 port 57447 ssh2
Jun 03 21:29:39 farnsworth sshd[28642]: Received disconnect from 116.31.116.15 port 57447:11:  [preauth]
Jun 03 21:29:39 farnsworth sshd[28642]: Disconnected from 116.31.116.15 port 57447 [preauth]
Jun 03 21:29:39 farnsworth sshd[28642]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:30:19 farnsworth sshd[28649]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:30:19 farnsworth sshd[28649]: input_userauth_request: invalid user root [preauth]
Jun 03 21:30:19 farnsworth sshd[28649]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:30:19 farnsworth sshd[28649]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:30:21 farnsworth sshd[28649]: Failed password for invalid user root from 116.31.116.15 port 22512 ssh2
Jun 03 21:30:21 farnsworth sshd[28649]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:30:24 farnsworth sshd[28649]: Failed password for invalid user root from 116.31.116.15 port 22512 ssh2
Jun 03 21:30:24 farnsworth sshd[28649]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:30:26 farnsworth sshd[28649]: Failed password for invalid user root from 116.31.116.15 port 22512 ssh2
Jun 03 21:30:27 farnsworth sshd[28649]: Received disconnect from 116.31.116.15 port 22512:11:  [preauth]
Jun 03 21:30:27 farnsworth sshd[28649]: Disconnected from 116.31.116.15 port 22512 [preauth]
Jun 03 21:30:27 farnsworth sshd[28649]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:31:04 farnsworth sshd[28653]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:31:04 farnsworth sshd[28653]: input_userauth_request: invalid user root [preauth]
Jun 03 21:31:04 farnsworth sshd[28653]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:31:04 farnsworth sshd[28653]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:31:05 farnsworth sshd[28653]: Failed password for invalid user root from 116.31.116.15 port 64625 ssh2
Jun 03 21:31:05 farnsworth sshd[28653]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:31:08 farnsworth sshd[28653]: Failed password for invalid user root from 116.31.116.15 port 64625 ssh2
Jun 03 21:31:08 farnsworth sshd[28653]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:31:10 farnsworth sshd[28653]: Failed password for invalid user root from 116.31.116.15 port 64625 ssh2
Jun 03 21:31:10 farnsworth sshd[28653]: Received disconnect from 116.31.116.15 port 64625:11:  [preauth]
Jun 03 21:31:10 farnsworth sshd[28653]: Disconnected from 116.31.116.15 port 64625 [preauth]
Jun 03 21:31:10 farnsworth sshd[28653]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:31:50 farnsworth sshd[28656]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:31:50 farnsworth sshd[28656]: input_userauth_request: invalid user root [preauth]
Jun 03 21:31:50 farnsworth sshd[28656]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:31:50 farnsworth sshd[28656]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:31:51 farnsworth sshd[28656]: Failed password for invalid user root from 116.31.116.15 port 17722 ssh2
Jun 03 21:31:52 farnsworth sshd[28656]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:31:54 farnsworth sshd[28656]: Failed password for invalid user root from 116.31.116.15 port 17722 ssh2
Jun 03 21:31:54 farnsworth sshd[28656]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:31:57 farnsworth sshd[28656]: Failed password for invalid user root from 116.31.116.15 port 17722 ssh2
Jun 03 21:31:57 farnsworth sshd[28656]: Received disconnect from 116.31.116.15 port 17722:11:  [preauth]
Jun 03 21:31:57 farnsworth sshd[28656]: Disconnected from 116.31.116.15 port 17722 [preauth]
Jun 03 21:31:57 farnsworth sshd[28656]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:32:36 farnsworth sshd[28662]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:32:36 farnsworth sshd[28662]: input_userauth_request: invalid user root [preauth]
Jun 03 21:32:36 farnsworth sshd[28662]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:32:36 farnsworth sshd[28662]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:32:38 farnsworth sshd[28662]: Failed password for invalid user root from 116.31.116.15 port 30228 ssh2
Jun 03 21:32:38 farnsworth sshd[28662]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:32:40 farnsworth sshd[28662]: Failed password for invalid user root from 116.31.116.15 port 30228 ssh2
Jun 03 21:32:40 farnsworth sshd[28662]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:32:42 farnsworth sshd[28662]: Failed password for invalid user root from 116.31.116.15 port 30228 ssh2
Jun 03 21:32:42 farnsworth sshd[28662]: Received disconnect from 116.31.116.15 port 30228:11:  [preauth]
Jun 03 21:32:42 farnsworth sshd[28662]: Disconnected from 116.31.116.15 port 30228 [preauth]
Jun 03 21:32:42 farnsworth sshd[28662]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:33:20 farnsworth sshd[28674]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 21:33:20 farnsworth sshd[28674]: input_userauth_request: invalid user root [preauth]
Jun 03 21:33:21 farnsworth sshd[28674]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:33:21 farnsworth sshd[28674]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 21:33:22 farnsworth sshd[28674]: Failed password for invalid user root from 116.31.116.15 port 36020 ssh2
Jun 03 21:33:23 farnsworth sshd[28674]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 21:33:24 farnsworth sshd[28674]: Failed password for invalid user root from 116.31.116.15 port 36020 ssh2
Jun 03 21:33:24 farnsworth sshd[28674]: pam_tally(sshd:auth): Tally overflowed for user root
"""

one_session = """
Jun 04 22:04:29 farnsworth sshd[9802]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:04:29 farnsworth sshd[9802]: input_userauth_request: invalid user root [preauth]
Jun 04 22:04:30 farnsworth sshd[9802]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:30 farnsworth sshd[9802]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:04:32 farnsworth sshd[9802]: Failed password for invalid user root from 218.65.30.126 port 65188 ssh2
Jun 04 22:04:32 farnsworth sshd[9802]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:34 farnsworth sshd[9804]: Accepted password for nancy from 192.168.0.110 port 47996 ssh2
Jun 04 22:04:34 farnsworth sshd[9804]: pam_unix(sshd:session): session opened for user nancy by (uid=0)
Jun 04 22:04:34 farnsworth sshd[9802]: Failed password for invalid user root from 218.65.30.126 port 65188 ssh2
Jun 04 22:04:35 farnsworth sshd[9802]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:38 farnsworth sshd[9802]: Failed password for invalid user root from 218.65.30.126 port 65188 ssh2
Jun 04 22:04:40 farnsworth sshd[9802]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 65188 ssh2 [preauth]
Jun 04 22:04:40 farnsworth sshd[9802]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:04:40 farnsworth sshd[9802]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
"""

two_sessions = """
Jun 04 22:04:34 farnsworth sshd[9804]: Accepted password for nancy from 192.168.0.110 port 47996 ssh2
Jun 04 22:04:34 farnsworth sshd[9804]: pam_unix(sshd:session): session opened for user nancy by (uid=0)
Jun 04 22:04:34 farnsworth sshd[9802]: Failed password for invalid user root from 218.65.30.126 port 65188 ssh2
Jun 04 22:04:35 farnsworth sshd[9802]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:38 farnsworth sshd[9802]: Failed password for invalid user root from 218.65.30.126 port 65188 ssh2
Jun 04 22:04:40 farnsworth sshd[9802]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 65188 ssh2 [preauth]
Jun 04 22:04:40 farnsworth sshd[9802]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:04:40 farnsworth sshd[9802]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:04:43 farnsworth sshd[9827]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:04:43 farnsworth sshd[9827]: input_userauth_request: invalid user root [preauth]
Jun 04 22:04:44 farnsworth sshd[9827]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:44 farnsworth sshd[9827]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:04:46 farnsworth sshd[9827]: Failed password for invalid user root from 218.65.30.126 port 3462 ssh2
Jun 04 22:04:47 farnsworth sshd[9827]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:49 farnsworth sshd[9827]: Failed password for invalid user root from 218.65.30.126 port 3462 ssh2
Jun 04 22:04:53 farnsworth sshd[9827]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:55 farnsworth sshd[9827]: Failed password for invalid user root from 218.65.30.126 port 3462 ssh2
Jun 04 22:04:58 farnsworth sshd[9827]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 3462 ssh2 [preauth]
Jun 04 22:04:58 farnsworth sshd[9827]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:04:58 farnsworth sshd[9827]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:01 farnsworth sshd[9837]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:05:01 farnsworth sshd[9837]: input_userauth_request: invalid user root [preauth]
Jun 04 22:05:01 farnsworth sshd[9837]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:01 farnsworth sshd[9837]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:03 farnsworth sshd[9837]: Failed password for invalid user root from 218.65.30.126 port 29160 ssh2
Jun 04 22:05:04 farnsworth sshd[9837]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:06 farnsworth sshd[9837]: Failed password for invalid user root from 218.65.30.126 port 29160 ssh2
Jun 04 22:05:07 farnsworth sshd[9837]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:09 farnsworth sshd[9837]: Failed password for invalid user root from 218.65.30.126 port 29160 ssh2
Jun 04 22:05:11 farnsworth sshd[9837]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 29160 ssh2 [preauth]
Jun 04 22:05:11 farnsworth sshd[9837]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:05:11 farnsworth sshd[9837]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:19 farnsworth sshd[9844]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:05:19 farnsworth sshd[9844]: input_userauth_request: invalid user root [preauth]
Jun 04 22:05:19 farnsworth sshd[9844]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:19 farnsworth sshd[9844]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:21 farnsworth sshd[9844]: Failed password for invalid user root from 218.65.30.126 port 49992 ssh2
Jun 04 22:05:22 farnsworth sshd[9844]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:24 farnsworth sshd[9844]: Failed password for invalid user root from 218.65.30.126 port 49992 ssh2
Jun 04 22:05:25 farnsworth sshd[9844]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:28 farnsworth sshd[9844]: Failed password for invalid user root from 218.65.30.126 port 49992 ssh2
Jun 04 22:05:30 farnsworth sshd[9844]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 49992 ssh2 [preauth]
Jun 04 22:05:30 farnsworth sshd[9844]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:05:30 farnsworth sshd[9844]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:34 farnsworth sshd[9846]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:05:34 farnsworth sshd[9846]: input_userauth_request: invalid user root [preauth]
Jun 04 22:05:34 farnsworth sshd[9846]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:34 farnsworth sshd[9846]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:37 farnsworth sshd[9846]: Failed password for invalid user root from 218.65.30.126 port 58368 ssh2
Jun 04 22:05:37 farnsworth sshd[9846]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:40 farnsworth sshd[9846]: Failed password for invalid user root from 218.65.30.126 port 58368 ssh2
Jun 04 22:05:41 farnsworth sshd[9846]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:43 farnsworth sshd[9846]: Failed password for invalid user root from 218.65.30.126 port 58368 ssh2
Jun 04 22:05:46 farnsworth sshd[9846]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 58368 ssh2 [preauth]
Jun 04 22:05:46 farnsworth sshd[9846]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:05:46 farnsworth sshd[9846]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:49 farnsworth sshd[9849]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:05:49 farnsworth sshd[9849]: input_userauth_request: invalid user root [preauth]
Jun 04 22:05:49 farnsworth sshd[9849]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:49 farnsworth sshd[9849]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:51 farnsworth sshd[9849]: Failed password for invalid user root from 218.65.30.126 port 18888 ssh2
Jun 04 22:05:52 farnsworth sshd[9849]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:54 farnsworth sshd[9849]: Failed password for invalid user root from 218.65.30.126 port 18888 ssh2
Jun 04 22:05:55 farnsworth sshd[9849]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:57 farnsworth sshd[9849]: Failed password for invalid user root from 218.65.30.126 port 18888 ssh2
Jun 04 22:05:59 farnsworth sshd[9849]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 18888 ssh2 [preauth]
Jun 04 22:05:59 farnsworth sshd[9849]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:05:59 farnsworth sshd[9849]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:00 farnsworth sshd[9852]: Connection closed by 192.168.0.112 port 48068 [preauth]
Jun 04 22:06:00 farnsworth sshd[9854]: Connection closed by 192.168.0.112 port 48070 [preauth]
Jun 04 22:06:00 farnsworth sshd[9856]: Connection closed by 192.168.0.112 port 48072 [preauth]
Jun 04 22:06:02 farnsworth sshd[9860]: Connection closed by 192.168.0.112 port 48074 [preauth]
Jun 04 22:06:02 farnsworth sshd[9862]: Connection closed by 192.168.0.112 port 48076 [preauth]
Jun 04 22:06:02 farnsworth sshd[9864]: Connection closed by 192.168.0.112 port 48078 [preauth]
Jun 04 22:06:02 farnsworth sshd[9858]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:06:02 farnsworth sshd[9858]: input_userauth_request: invalid user root [preauth]
Jun 04 22:06:03 farnsworth sshd[9858]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:03 farnsworth sshd[9858]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:05 farnsworth sshd[9858]: Failed password for invalid user root from 218.65.30.126 port 22014 ssh2
Jun 04 22:06:05 farnsworth sshd[9866]: Connection closed by 192.168.0.112 port 48080 [preauth]
Jun 04 22:06:05 farnsworth sshd[9868]: Connection closed by 192.168.0.112 port 48082 [preauth]
Jun 04 22:06:05 farnsworth sshd[9858]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:08 farnsworth sshd[9858]: Failed password for invalid user root from 218.65.30.126 port 22014 ssh2
Jun 04 22:06:09 farnsworth sshd[9858]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:11 farnsworth sshd[9858]: Failed password for invalid user root from 218.65.30.126 port 22014 ssh2
Jun 04 22:06:13 farnsworth sshd[9858]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 22014 ssh2 [preauth]
Jun 04 22:06:13 farnsworth sshd[9858]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:06:13 farnsworth sshd[9858]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:16 farnsworth sshd[9808]: Received disconnect from 192.168.0.112 port 47996:11: disconnected by user
Jun 04 22:06:16 farnsworth sshd[9871]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:06:16 farnsworth sshd[9871]: input_userauth_request: invalid user root [preauth]
Jun 04 22:06:17 farnsworth sshd[9871]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:17 farnsworth sshd[9871]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:18 farnsworth sshd[9875]: Connection closed by 192.168.0.112 port 48084 [preauth]
Jun 04 22:06:18 farnsworth sshd[9877]: Connection closed by 192.168.0.112 port 48086 [preauth]
Jun 04 22:06:19 farnsworth sshd[9879]: Connection closed by 192.168.0.112 port 48088 [preauth]
Jun 04 22:06:19 farnsworth sshd[9871]: Failed password for invalid user root from 218.65.30.126 port 46623 ssh2
Jun 04 22:06:20 farnsworth sshd[9871]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:22 farnsworth sshd[9871]: Failed password for invalid user root from 218.65.30.126 port 46623 ssh2
Jun 04 22:06:23 farnsworth sshd[9871]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:23 farnsworth sshd[9881]: Connection closed by 192.168.0.112 port 48094 [preauth]
Jun 04 22:06:23 farnsworth sshd[9883]: Connection closed by 192.168.0.112 port 48096 [preauth]
Jun 04 22:06:23 farnsworth sshd[9885]: Connection closed by 192.168.0.112 port 48098 [preauth]
Jun 04 22:06:25 farnsworth sshd[9871]: Failed password for invalid user root from 218.65.30.126 port 46623 ssh2
Jun 04 22:06:27 farnsworth sshd[9871]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 46623 ssh2 [preauth]
Jun 04 22:06:27 farnsworth sshd[9871]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:06:27 farnsworth sshd[9871]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:31 farnsworth sshd[9889]: Connection closed by 192.168.0.112 port 48100 [preauth]
Jun 04 22:06:31 farnsworth sshd[9887]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:06:31 farnsworth sshd[9887]: input_userauth_request: invalid user root [preauth]
Jun 04 22:06:31 farnsworth sshd[9891]: Connection closed by 192.168.0.112 port 48102 [preauth]
Jun 04 22:06:31 farnsworth sshd[9893]: Connection closed by 192.168.0.112 port 48104 [preauth]
Jun 04 22:06:31 farnsworth sshd[9887]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:31 farnsworth sshd[9887]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:33 farnsworth sshd[9887]: Failed password for invalid user root from 218.65.30.126 port 49663 ssh2
Jun 04 22:06:34 farnsworth sshd[9887]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:36 farnsworth sshd[9887]: Failed password for invalid user root from 218.65.30.126 port 49663 ssh2
Jun 04 22:06:37 farnsworth sshd[9887]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:39 farnsworth sshd[9887]: Failed password for invalid user root from 218.65.30.126 port 49663 ssh2
Jun 04 22:06:41 farnsworth sshd[9887]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 49663 ssh2 [preauth]
Jun 04 22:06:41 farnsworth sshd[9887]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:06:41 farnsworth sshd[9887]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:45 farnsworth sshd[9895]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:06:45 farnsworth sshd[9895]: input_userauth_request: invalid user root [preauth]
Jun 04 22:06:45 farnsworth sshd[9895]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:45 farnsworth sshd[9895]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:47 farnsworth sshd[9895]: Failed password for invalid user root from 218.65.30.126 port 9815 ssh2
Jun 04 22:06:48 farnsworth sshd[9895]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:49 farnsworth sshd[9895]: Failed password for invalid user root from 218.65.30.126 port 9815 ssh2
Jun 04 22:06:50 farnsworth sshd[9895]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:53 farnsworth sshd[9895]: Failed password for invalid user root from 218.65.30.126 port 9815 ssh2
Jun 04 22:06:55 farnsworth sshd[9895]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 9815 ssh2 [preauth]
Jun 04 22:06:55 farnsworth sshd[9895]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:06:55 farnsworth sshd[9895]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:07:05 farnsworth sshd[9903]: Connection closed by 192.168.0.112 port 48112 [preauth]
Jun 04 22:07:05 farnsworth sshd[9905]: Connection closed by 192.168.0.112 port 48114 [preauth]
Jun 04 22:07:06 farnsworth sshd[9901]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:07:06 farnsworth sshd[9901]: input_userauth_request: invalid user root [preauth]
Jun 04 22:07:07 farnsworth sshd[9901]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:07:07 farnsworth sshd[9901]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:07:07 farnsworth sshd[9907]: Accepted password for taylor from 192.168.0.113 port 48116 ssh2
Jun 04 22:07:07 farnsworth sshd[9907]: pam_unix(sshd:session): session opened for user taylor by (uid=0)
Jun 04 22:07:07 farnsworth sshd[9909]: Received disconnect from 192.168.0.113 port 48116:11: disconnected by user
Jun 04 22:07:07 farnsworth sshd[9909]: Disconnected from 192.168.0.113 port 48116
Jun 04 22:07:07 farnsworth sshd[9907]: pam_unix(sshd:session): session closed for user taylor
"""

eight_sessions = """
Jun 04 22:04:34 farnsworth sshd[9804]: Accepted password for nancy from 192.168.0.110 port 47996 ssh2
Jun 04 22:04:34 farnsworth sshd[9804]: pam_unix(sshd:session): session opened for user nancy by (uid=0)
Jun 04 22:04:34 farnsworth sshd[9802]: Failed password for invalid user root from 218.65.30.126 port 65188 ssh2
Jun 04 22:04:35 farnsworth sshd[9802]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:38 farnsworth sshd[9802]: Failed password for invalid user root from 218.65.30.126 port 65188 ssh2
Jun 04 22:04:40 farnsworth sshd[9802]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 65188 ssh2 [preauth]
Jun 04 22:04:40 farnsworth sshd[9802]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:04:40 farnsworth sshd[9802]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:04:43 farnsworth sshd[9827]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:04:43 farnsworth sshd[9827]: input_userauth_request: invalid user root [preauth]
Jun 04 22:04:44 farnsworth sshd[9827]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:44 farnsworth sshd[9827]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:04:46 farnsworth sshd[9827]: Failed password for invalid user root from 218.65.30.126 port 3462 ssh2
Jun 04 22:04:47 farnsworth sshd[9827]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:49 farnsworth sshd[9827]: Failed password for invalid user root from 218.65.30.126 port 3462 ssh2
Jun 04 22:04:53 farnsworth sshd[9827]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:04:55 farnsworth sshd[9827]: Failed password for invalid user root from 218.65.30.126 port 3462 ssh2
Jun 04 22:04:58 farnsworth sshd[9827]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 3462 ssh2 [preauth]
Jun 04 22:04:58 farnsworth sshd[9827]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:04:58 farnsworth sshd[9827]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:01 farnsworth sshd[9837]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:05:01 farnsworth sshd[9837]: input_userauth_request: invalid user root [preauth]
Jun 04 22:05:01 farnsworth sshd[9837]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:01 farnsworth sshd[9837]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:03 farnsworth sshd[9837]: Failed password for invalid user root from 218.65.30.126 port 29160 ssh2
Jun 04 22:05:04 farnsworth sshd[9837]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:06 farnsworth sshd[9837]: Failed password for invalid user root from 218.65.30.126 port 29160 ssh2
Jun 04 22:05:07 farnsworth sshd[9837]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:09 farnsworth sshd[9837]: Failed password for invalid user root from 218.65.30.126 port 29160 ssh2
Jun 04 22:05:11 farnsworth sshd[9837]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 29160 ssh2 [preauth]
Jun 04 22:05:11 farnsworth sshd[9837]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:05:11 farnsworth sshd[9837]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:19 farnsworth sshd[9844]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:05:19 farnsworth sshd[9844]: input_userauth_request: invalid user root [preauth]
Jun 04 22:05:19 farnsworth sshd[9844]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:19 farnsworth sshd[9844]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:21 farnsworth sshd[9844]: Failed password for invalid user root from 218.65.30.126 port 49992 ssh2
Jun 04 22:05:22 farnsworth sshd[9844]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:24 farnsworth sshd[9844]: Failed password for invalid user root from 218.65.30.126 port 49992 ssh2
Jun 04 22:05:25 farnsworth sshd[9844]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:28 farnsworth sshd[9844]: Failed password for invalid user root from 218.65.30.126 port 49992 ssh2
Jun 04 22:05:30 farnsworth sshd[9844]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 49992 ssh2 [preauth]
Jun 04 22:05:30 farnsworth sshd[9844]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:05:30 farnsworth sshd[9844]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:34 farnsworth sshd[9846]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:05:34 farnsworth sshd[9846]: input_userauth_request: invalid user root [preauth]
Jun 04 22:05:34 farnsworth sshd[9846]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:34 farnsworth sshd[9846]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:37 farnsworth sshd[9846]: Failed password for invalid user root from 218.65.30.126 port 58368 ssh2
Jun 04 22:05:37 farnsworth sshd[9846]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:40 farnsworth sshd[9846]: Failed password for invalid user root from 218.65.30.126 port 58368 ssh2
Jun 04 22:05:41 farnsworth sshd[9846]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:43 farnsworth sshd[9846]: Failed password for invalid user root from 218.65.30.126 port 58368 ssh2
Jun 04 22:05:46 farnsworth sshd[9846]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 58368 ssh2 [preauth]
Jun 04 22:05:46 farnsworth sshd[9846]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:05:46 farnsworth sshd[9846]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:49 farnsworth sshd[9849]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:05:49 farnsworth sshd[9849]: input_userauth_request: invalid user root [preauth]
Jun 04 22:05:49 farnsworth sshd[9849]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:49 farnsworth sshd[9849]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:05:51 farnsworth sshd[9849]: Failed password for invalid user root from 218.65.30.126 port 18888 ssh2
Jun 04 22:05:52 farnsworth sshd[9849]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:54 farnsworth sshd[9849]: Failed password for invalid user root from 218.65.30.126 port 18888 ssh2
Jun 04 22:05:55 farnsworth sshd[9849]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:05:57 farnsworth sshd[9849]: Failed password for invalid user root from 218.65.30.126 port 18888 ssh2
Jun 04 22:05:59 farnsworth sshd[9849]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 18888 ssh2 [preauth]
Jun 04 22:05:59 farnsworth sshd[9849]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:05:59 farnsworth sshd[9849]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:00 farnsworth sshd[9852]: Connection closed by 192.168.0.112 port 48068 [preauth]
Jun 04 22:06:00 farnsworth sshd[9854]: Connection closed by 192.168.0.112 port 48070 [preauth]
Jun 04 22:06:00 farnsworth sshd[9856]: Connection closed by 192.168.0.112 port 48072 [preauth]
Jun 04 22:06:02 farnsworth sshd[9860]: Connection closed by 192.168.0.112 port 48074 [preauth]
Jun 04 22:06:02 farnsworth sshd[9862]: Connection closed by 192.168.0.112 port 48076 [preauth]
Jun 04 22:06:02 farnsworth sshd[9864]: Connection closed by 192.168.0.112 port 48078 [preauth]
Jun 04 22:06:02 farnsworth sshd[9858]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:06:02 farnsworth sshd[9858]: input_userauth_request: invalid user root [preauth]
Jun 04 22:06:03 farnsworth sshd[9858]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:03 farnsworth sshd[9858]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:05 farnsworth sshd[9858]: Failed password for invalid user root from 218.65.30.126 port 22014 ssh2
Jun 04 22:06:05 farnsworth sshd[9866]: Connection closed by 192.168.0.112 port 48080 [preauth]
Jun 04 22:06:05 farnsworth sshd[9868]: Connection closed by 192.168.0.112 port 48082 [preauth]
Jun 04 22:06:05 farnsworth sshd[9858]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:08 farnsworth sshd[9858]: Failed password for invalid user root from 218.65.30.126 port 22014 ssh2
Jun 04 22:06:09 farnsworth sshd[9858]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:11 farnsworth sshd[9858]: Failed password for invalid user root from 218.65.30.126 port 22014 ssh2
Jun 04 22:06:13 farnsworth sshd[9858]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 22014 ssh2 [preauth]
Jun 04 22:06:13 farnsworth sshd[9858]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:06:13 farnsworth sshd[9858]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:16 farnsworth sshd[9808]: Received disconnect from 192.168.0.112 port 47996:11: disconnected by user
Jun 04 22:06:16 farnsworth sshd[9871]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:06:16 farnsworth sshd[9871]: input_userauth_request: invalid user root [preauth]
Jun 04 22:06:17 farnsworth sshd[9871]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:17 farnsworth sshd[9871]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:18 farnsworth sshd[9875]: Connection closed by 192.168.0.112 port 48084 [preauth]
Jun 04 22:06:18 farnsworth sshd[9877]: Connection closed by 192.168.0.112 port 48086 [preauth]
Jun 04 22:06:19 farnsworth sshd[9879]: Connection closed by 192.168.0.112 port 48088 [preauth]
Jun 04 22:06:19 farnsworth sshd[9871]: Failed password for invalid user root from 218.65.30.126 port 46623 ssh2
Jun 04 22:06:20 farnsworth sshd[9871]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:22 farnsworth sshd[9871]: Failed password for invalid user root from 218.65.30.126 port 46623 ssh2
Jun 04 22:06:23 farnsworth sshd[9871]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:23 farnsworth sshd[9881]: Connection closed by 192.168.0.112 port 48094 [preauth]
Jun 04 22:06:23 farnsworth sshd[9883]: Connection closed by 192.168.0.112 port 48096 [preauth]
Jun 04 22:06:23 farnsworth sshd[9885]: Connection closed by 192.168.0.112 port 48098 [preauth]
Jun 04 22:06:25 farnsworth sshd[9871]: Failed password for invalid user root from 218.65.30.126 port 46623 ssh2
Jun 04 22:06:27 farnsworth sshd[9871]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 46623 ssh2 [preauth]
Jun 04 22:06:27 farnsworth sshd[9871]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:06:27 farnsworth sshd[9871]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:31 farnsworth sshd[9889]: Connection closed by 192.168.0.112 port 48100 [preauth]
Jun 04 22:06:31 farnsworth sshd[9887]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:06:31 farnsworth sshd[9887]: input_userauth_request: invalid user root [preauth]
Jun 04 22:06:31 farnsworth sshd[9891]: Connection closed by 192.168.0.112 port 48102 [preauth]
Jun 04 22:06:31 farnsworth sshd[9893]: Connection closed by 192.168.0.112 port 48104 [preauth]
Jun 04 22:06:31 farnsworth sshd[9887]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:31 farnsworth sshd[9887]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:33 farnsworth sshd[9887]: Failed password for invalid user root from 218.65.30.126 port 49663 ssh2
Jun 04 22:06:34 farnsworth sshd[9887]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:36 farnsworth sshd[9887]: Failed password for invalid user root from 218.65.30.126 port 49663 ssh2
Jun 04 22:06:37 farnsworth sshd[9887]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:39 farnsworth sshd[9887]: Failed password for invalid user root from 218.65.30.126 port 49663 ssh2
Jun 04 22:06:41 farnsworth sshd[9887]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 49663 ssh2 [preauth]
Jun 04 22:06:41 farnsworth sshd[9887]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:06:41 farnsworth sshd[9887]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:45 farnsworth sshd[9895]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:06:45 farnsworth sshd[9895]: input_userauth_request: invalid user root [preauth]
Jun 04 22:06:45 farnsworth sshd[9895]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:45 farnsworth sshd[9895]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:06:47 farnsworth sshd[9895]: Failed password for invalid user root from 218.65.30.126 port 9815 ssh2
Jun 04 22:06:48 farnsworth sshd[9895]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:49 farnsworth sshd[9895]: Failed password for invalid user root from 218.65.30.126 port 9815 ssh2
Jun 04 22:06:50 farnsworth sshd[9895]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:06:53 farnsworth sshd[9895]: Failed password for invalid user root from 218.65.30.126 port 9815 ssh2
Jun 04 22:06:55 farnsworth sshd[9895]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 9815 ssh2 [preauth]
Jun 04 22:06:55 farnsworth sshd[9895]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:06:55 farnsworth sshd[9895]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:07:05 farnsworth sshd[9903]: Connection closed by 192.168.0.112 port 48112 [preauth]
Jun 04 22:07:05 farnsworth sshd[9905]: Connection closed by 192.168.0.112 port 48114 [preauth]
Jun 04 22:07:06 farnsworth sshd[9901]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:07:06 farnsworth sshd[9901]: input_userauth_request: invalid user root [preauth]
Jun 04 22:07:07 farnsworth sshd[9901]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:07:07 farnsworth sshd[9901]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:07:07 farnsworth sshd[9907]: Accepted password for taylor from 192.168.0.113 port 48116 ssh2
Jun 04 22:07:07 farnsworth sshd[9907]: pam_unix(sshd:session): session opened for user taylor by (uid=0)
Jun 04 22:07:07 farnsworth sshd[9909]: Received disconnect from 192.168.0.113 port 48116:11: disconnected by user
Jun 04 22:07:07 farnsworth sshd[9909]: Disconnected from 192.168.0.113 port 48116
Jun 04 22:07:07 farnsworth sshd[9907]: pam_unix(sshd:session): session closed for user taylor
Jun 04 22:07:09 farnsworth sshd[9901]: Failed password for invalid user root from 218.65.30.126 port 13030 ssh2
Jun 04 22:07:10 farnsworth sshd[9901]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:07:12 farnsworth sshd[9901]: Failed password for invalid user root from 218.65.30.126 port 13030 ssh2
Jun 04 22:07:13 farnsworth sshd[9901]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:07:13 farnsworth sshd[9917]: Invalid user student from 112.217.49.149 port 63467
Jun 04 22:07:13 farnsworth sshd[9917]: input_userauth_request: invalid user student [preauth]
Jun 04 22:07:14 farnsworth sshd[9917]: pam_tally(sshd:auth): pam_get_uid; no such user
Jun 04 22:07:14 farnsworth sshd[9917]: pam_unix(sshd:auth): check pass; user unknown
Jun 04 22:07:14 farnsworth sshd[9917]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=112.217.49.149
Jun 04 22:07:14 farnsworth sshd[9919]: Accepted publickey for taylor from 192.168.0.113 port 48118 ssh2: RSA SHA256:N3jQnh0rQrt9dBGV3sN4EXkxsYo132q6rRhoRgrzfDo
Jun 04 22:07:14 farnsworth sshd[9919]: pam_unix(sshd:session): session opened for user taylor by (uid=0)
Jun 04 22:07:15 farnsworth sshd[9901]: Failed password for invalid user root from 218.65.30.126 port 13030 ssh2
Jun 04 22:07:16 farnsworth sshd[9917]: Failed password for invalid user student from 112.217.49.149 port 63467 ssh2
Jun 04 22:07:16 farnsworth sshd[9917]: error: Received disconnect from 112.217.49.149 port 63467:3: com.jcraft.jsch.JSchException: Auth fail [preauth]
Jun 04 22:07:16 farnsworth sshd[9917]: Disconnected from 112.217.49.149 port 63467 [preauth]
Jun 04 22:07:16 farnsworth sshd[9921]: Received disconnect from 192.168.0.113 port 48118:11: disconnected by user
Jun 04 22:07:16 farnsworth sshd[9921]: Disconnected from 192.168.0.113 port 48118
Jun 04 22:07:16 farnsworth sshd[9919]: pam_unix(sshd:session): session closed for user taylor
Jun 04 22:07:18 farnsworth sshd[9901]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 13030 ssh2 [preauth]
Jun 04 22:07:18 farnsworth sshd[9901]: Disconnecting: Too many authentication failures [preauth]
Jun 04 22:07:18 farnsworth sshd[9901]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:07:19 farnsworth sshd[9941]: Accepted publickey for taylor from 192.168.0.113 port 48120 ssh2: RSA SHA256:N3jQnh0rQrt9dBGV3sN4EXkxsYo132q6rRhoRgrzfDo
Jun 04 22:07:19 farnsworth sshd[9941]: pam_unix(sshd:session): session opened for user taylor by (uid=0)
Jun 04 22:07:19 farnsworth sshd[9943]: Received disconnect from 192.168.0.113 port 48120:11: disconnected by user
Jun 04 22:07:19 farnsworth sshd[9943]: Disconnected from 192.168.0.113 port 48120
Jun 04 22:07:19 farnsworth sshd[9941]: pam_unix(sshd:session): session closed for user taylor
Jun 04 22:07:20 farnsworth sshd[9948]: Accepted publickey for taylor from 192.168.0.113 port 48122 ssh2: RSA SHA256:N3jQnh0rQrt9dBGV3sN4EXkxsYo132q6rRhoRgrzfDo
Jun 04 22:07:20 farnsworth sshd[9948]: pam_unix(sshd:session): session opened for user taylor by (uid=0)
Jun 04 22:07:20 farnsworth sshd[9950]: Received disconnect from 192.168.0.113 port 48122:11: disconnected by user
Jun 04 22:07:20 farnsworth sshd[9950]: Disconnected from 192.168.0.113 port 48122
Jun 04 22:07:20 farnsworth sshd[9948]: pam_unix(sshd:session): session closed for user taylor
Jun 04 22:07:21 farnsworth sshd[9946]: User root from 218.65.30.126 not allowed because not listed in AllowUsers
Jun 04 22:07:21 farnsworth sshd[9946]: input_userauth_request: invalid user root [preauth]
Jun 04 22:07:21 farnsworth sshd[9946]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:07:21 farnsworth sshd[9946]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.65.30.126  user=root
Jun 04 22:07:21 farnsworth sshd[9953]: Accepted publickey for taylor from 192.168.0.113 port 48124 ssh2: RSA SHA256:N3jQnh0rQrt9dBGV3sN4EXkxsYo132q6rRhoRgrzfDo
Jun 04 22:07:21 farnsworth sshd[9953]: pam_unix(sshd:session): session opened for user taylor by (uid=0)
Jun 04 22:07:21 farnsworth sshd[9955]: Received disconnect from 192.168.0.113 port 48124:11: disconnected by user
Jun 04 22:07:21 farnsworth sshd[9955]: Disconnected from 192.168.0.113 port 48124
Jun 04 22:07:21 farnsworth sshd[9953]: pam_unix(sshd:session): session closed for user taylor
Jun 04 22:07:22 farnsworth sshd[9959]: Accepted publickey for taylor from 192.168.0.113 port 48126 ssh2: RSA SHA256:N3jQnh0rQrt9dBGV3sN4EXkxsYo132q6rRhoRgrzfDo
Jun 04 22:07:22 farnsworth sshd[9959]: pam_unix(sshd:session): session opened for user taylor by (uid=0)
Jun 04 22:07:22 farnsworth sshd[9961]: Received disconnect from 192.168.0.113 port 48126:11: disconnected by user
Jun 04 22:07:22 farnsworth sshd[9961]: Disconnected from 192.168.0.113 port 48126
Jun 04 22:07:22 farnsworth sshd[9959]: pam_unix(sshd:session): session closed for user taylor
Jun 04 22:07:23 farnsworth sshd[9946]: Failed password for invalid user root from 218.65.30.126 port 39013 ssh2
Jun 04 22:07:24 farnsworth sshd[9946]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:07:26 farnsworth sshd[9946]: Failed password for invalid user root from 218.65.30.126 port 39013 ssh2
Jun 04 22:07:26 farnsworth sshd[9946]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 04 22:07:28 farnsworth sshd[9946]: Failed password for invalid user root from 218.65.30.126 port 39013 ssh2
Jun 04 22:07:31 farnsworth sshd[9946]: error: maximum authentication attempts exceeded for invalid user root from 218.65.30.126 port 39013 ssh2 [preauth]
Jun 04 22:07:33 farnsworth sshd[9970]: Accepted publickey for virgil from 192.168.0.113 port 48128 ssh2: RSA SHA256:N3jQnh0rQrt9dBGV3sN4EXkxsYo132q6rRhoRgrzfDo
Jun 04 22:07:33 farnsworth sshd[9970]: pam_unix(sshd:session): session opened for user virgil by (uid=0)
"""

three_failed = """
Jun 03 22:37:20 farnsworth sshd[29209]: Failed password for invalid user root from 116.31.116.15 port 23267 ssh2
Jun 03 22:37:20 farnsworth sshd[29209]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:37:22 farnsworth sshd[29209]: Failed password for invalid user root from 116.31.116.15 port 23267 ssh2
Jun 03 22:37:22 farnsworth sshd[29209]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:37:24 farnsworth sshd[29209]: Failed password for invalid user root from 116.31.116.15 port 23267 ssh2
Jun 03 22:37:24 farnsworth sshd[29209]: Received disconnect from 116.31.116.15 port 23267:11:  [preauth]
Jun 03 22:37:24 farnsworth sshd[29209]: Disconnected from 116.31.116.15 port 23267 [preauth]
Jun 03 22:37:24 farnsworth sshd[29209]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 22:38:09 farnsworth sshd[29213]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 22:38:09 farnsworth sshd[29213]: input_userauth_request: invalid user root [preauth]
Jun 03 22:38:09 farnsworth sshd[29213]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:38:09 farnsworth sshd[29213]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 22:38:11 farnsworth sshd[29213]: Failed password for invalid user root from 116.31.116.15 port 52305 ssh2
Jun 03 22:38:11 farnsworth sshd[29213]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:38:13 farnsworth sshd[29213]: Failed password for invalid user root from 116.31.116.15 port 52305 ssh2
Jun 03 22:38:13 farnsworth sshd[29213]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:38:16 farnsworth sshd[29213]: Failed password for invalid user root from 116.31.116.15 port 52305 ssh2
Jun 03 22:38:16 farnsworth sshd[29213]: Received disconnect from 116.31.116.15 port 52305:11:  [preauth]
Jun 03 22:38:16 farnsworth sshd[29213]: Disconnected from 116.31.116.15 port 52305 [preauth]
Jun 03 22:38:16 farnsworth sshd[29213]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 22:38:38 farnsworth sshd[29217]: Invalid user pi from 112.217.49.149 port 51215
Jun 03 22:38:38 farnsworth sshd[29217]: input_userauth_request: invalid user pi [preauth]
Jun 03 22:38:38 farnsworth sshd[29217]: pam_tally(sshd:auth): pam_get_uid; no such user
Jun 03 22:38:38 farnsworth sshd[29217]: pam_unix(sshd:auth): check pass; user unknown
Jun 03 22:38:38 farnsworth sshd[29217]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=112.217.49.149
Jun 03 22:38:40 farnsworth sshd[29217]: Failed password for invalid user pi from 112.217.49.149 port 51215 ssh2
Jun 03 22:38:40 farnsworth sshd[29217]: error: Received disconnect from 112.217.49.149 port 51215:3: com.jcraft.jsch.JSchException: Auth fail [preauth]
Jun 03 22:38:40 farnsworth sshd[29217]: Disconnected from 112.217.49.149 port 51215 [preauth]
Jun 03 22:38:56 farnsworth sshd[29223]: Invalid user admin from 181.211.138.186 port 51187
Jun 03 22:38:56 farnsworth sshd[29223]: input_userauth_request: invalid user admin [preauth]
Jun 03 22:38:56 farnsworth sshd[29223]: pam_tally(sshd:auth): pam_get_uid; no such user
Jun 03 22:38:56 farnsworth sshd[29223]: pam_unix(sshd:auth): check pass; user unknown
Jun 03 22:38:56 farnsworth sshd[29223]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=181.211.138.186
Jun 03 22:38:57 farnsworth sshd[29225]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 22:38:57 farnsworth sshd[29225]: input_userauth_request: invalid user root [preauth]
Jun 03 22:38:57 farnsworth sshd[29225]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:38:57 farnsworth sshd[29225]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 22:38:59 farnsworth sshd[29223]: Failed password for invalid user admin from 181.211.138.186 port 51187 ssh2
Jun 03 22:38:59 farnsworth sshd[29225]: Failed password for invalid user root from 116.31.116.15 port 44351 ssh2
Jun 03 22:38:59 farnsworth sshd[29223]: pam_tally(sshd:auth): pam_get_uid; no such user
Jun 03 22:38:59 farnsworth sshd[29223]: pam_unix(sshd:auth): check pass; user unknown
Jun 03 22:38:59 farnsworth sshd[29225]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:39:01 farnsworth sshd[29223]: Failed password for invalid user admin from 181.211.138.186 port 51187 ssh2
Jun 03 22:39:01 farnsworth sshd[29225]: Failed password for invalid user root from 116.31.116.15 port 44351 ssh2
Jun 03 22:39:01 farnsworth sshd[29223]: pam_tally(sshd:auth): pam_get_uid; no such user
Jun 03 22:39:01 farnsworth sshd[29223]: pam_unix(sshd:auth): check pass; user unknown
Jun 03 22:39:01 farnsworth sshd[29225]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:39:03 farnsworth sshd[29223]: Failed password for invalid user admin from 181.211.138.186 port 51187 ssh2
Jun 03 22:39:04 farnsworth sshd[29225]: Failed password for invalid user root from 116.31.116.15 port 44351 ssh2
Jun 03 22:39:04 farnsworth sshd[29223]: pam_tally(sshd:auth): pam_get_uid; no such user
Jun 03 22:39:04 farnsworth sshd[29223]: pam_unix(sshd:auth): check pass; user unknown
Jun 03 22:39:04 farnsworth sshd[29225]: Received disconnect from 116.31.116.15 port 44351:11:  [preauth]
Jun 03 22:39:04 farnsworth sshd[29225]: Disconnected from 116.31.116.15 port 44351 [preauth]
Jun 03 22:39:04 farnsworth sshd[29225]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 22:39:06 farnsworth sshd[29223]: Failed password for invalid user admin from 181.211.138.186 port 51187 ssh2
Jun 03 22:39:06 farnsworth sshd[29223]: pam_tally(sshd:auth): pam_get_uid; no such user
Jun 03 22:39:06 farnsworth sshd[29223]: pam_unix(sshd:auth): check pass; user unknown
Jun 03 22:39:08 farnsworth sshd[29223]: Failed password for invalid user admin from 181.211.138.186 port 51187 ssh2
Jun 03 22:39:08 farnsworth sshd[29223]: pam_tally(sshd:auth): pam_get_uid; no such user
Jun 03 22:39:08 farnsworth sshd[29223]: pam_unix(sshd:auth): check pass; user unknown
Jun 03 22:39:10 farnsworth sshd[29223]: Failed password for invalid user admin from 181.211.138.186 port 51187 ssh2
Jun 03 22:39:10 farnsworth sshd[29223]: error: maximum authentication attempts exceeded for invalid user admin from 181.211.138.186 port 51187 ssh2 [preauth]
Jun 03 22:39:10 farnsworth sshd[29223]: Disconnecting: Too many authentication failures [preauth]
Jun 03 22:39:10 farnsworth sshd[29223]: PAM 5 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=181.211.138.186
Jun 03 22:39:10 farnsworth sshd[29223]: PAM service(sshd) ignoring max retries; 6 > 3
Jun 03 22:39:50 farnsworth sshd[29230]: User root from 116.31.116.15 not allowed because not listed in AllowUsers
Jun 03 22:39:50 farnsworth sshd[29230]: input_userauth_request: invalid user root [preauth]
Jun 03 22:39:50 farnsworth sshd[29230]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:39:50 farnsworth sshd[29230]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
Jun 03 22:39:53 farnsworth sshd[29230]: Failed password for invalid user root from 116.31.116.15 port 32710 ssh2
Jun 03 22:39:53 farnsworth sshd[29230]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:39:55 farnsworth sshd[29230]: Failed password for invalid user root from 116.31.116.15 port 32710 ssh2
Jun 03 22:39:55 farnsworth sshd[29230]: pam_tally(sshd:auth): Tally overflowed for user root
Jun 03 22:39:57 farnsworth sshd[29230]: Failed password for invalid user root from 116.31.116.15 port 32710 ssh2
Jun 03 22:39:57 farnsworth sshd[29230]: Received disconnect from 116.31.116.15 port 32710:11:  [preauth]
Jun 03 22:39:57 farnsworth sshd[29230]: Disconnected from 116.31.116.15 port 32710 [preauth]
Jun 03 22:39:57 farnsworth sshd[29230]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=116.31.116.15  user=root
"""

if __name__ == "__main__":
    unittest.main(verbosity=2)