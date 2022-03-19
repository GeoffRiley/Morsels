import gzip
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address, ip_address

ASSUMED_YEAR: int = 2017


@dataclass
class Session:
    pid: int = None
    user: str = None
    opened: datetime = None
    closed: datetime = None
    ip: IPv4Address = None


def get_user_logins(gzip_file: str):
    with gzip.open(gzip_file, 'rt') as fb:
        lines = fb.read()
        return set(re.findall(r'session opened for user (\w+)', lines))


def get_failed_logins(gzip_file: str):
    with gzip.open(gzip_file, 'rt') as fb:
        lines = fb.read()
        fails = defaultdict(list)
        for user, ip in re.findall(
                r'Failed password for invalid user (\w+) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
                lines):
            fails[ip].append(user)
        return fails


ACCEPTED_LINE = re.compile(
    r'''
    sshd\[(\d+)\]:                          # pid
    \s+
    Accepted
    \s+ 
    (?:password|publickey)                  # ignore connection type
    \s+
    for 
    \s+
    (\w+)                                   # username
    \s+
    from 
    \s+
    (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})    # ip address
    ''', re.VERBOSE)
OPENED_LINE = re.compile(
    r'''
    (\w{3}\s\d\d\s\d\d:\d\d:\d\d)           # opened timestamp
    \s+
    \w+
    \s+
    sshd\[(\d+)\]:                          # pid
    .+:                                     # gobble up the session type
    \s+
    session\s+opened\s+for\s+user\s+
    (\w+)                                   # username
    ''', re.VERBOSE)
CLOSED_LINE = re.compile(
    r'''
    (\w{3}\s\d\d\s\d\d:\d\d:\d\d)           # closed timestamp
    \s+
    \w+
    \s+
    sshd\[(\d+)\]:                          # pid
    .+:                                     # gobble up the session type
    \s+
    session\s+closed\s+for\s+user\s+
    (\w+)                                   # username
    ''', re.VERBOSE)


def get_sessions(gzip_file: str, year: int = ASSUMED_YEAR):
    with gzip.open(gzip_file, 'rt') as fb:
        sessions = defaultdict(Session)
        for line in fb.read().splitlines(keepends=False):
            if match := ACCEPTED_LINE.search(line):
                pid, user, ip = match.groups()
                sessions[pid].pid = int(pid)
                sessions[pid].user = user
                sessions[pid].ip = ip_address(ip)
            elif match := OPENED_LINE.search(line):
                opened, pid, user = match.groups()
                sessions[pid].pid = int(pid)
                sessions[pid].opened = datetime.strptime(
                    f'{year} {opened}', '%Y %b %d %H:%M:%S')
                sessions[pid].user = user
            elif match := CLOSED_LINE.search(line):
                closed, pid, user = match.groups()
                sessions[pid].pid = int(pid)
                sessions[pid].closed = datetime.strptime(
                    f'{year} {closed}', '%Y %b %d %H:%M:%S')
                sessions[pid].user = user

        for s in sessions.values():
            if s.opened:
                yield s
