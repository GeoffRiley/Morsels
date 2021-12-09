"""
Adapted from https://stackoverflow.com/questions/748675/finding-duplicate-files-and-removing-them/36113168#36113168
"""
import hashlib
from collections import defaultdict
from pathlib import Path
from typing import List


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(file: Path, first_chunk_only=False, hash_algo=hashlib.sha1):
    hashobj = hash_algo()
    with file.open("rb") as f:
        if first_chunk_only:
            hashobj.update(f.read(1024))
        else:
            for chunk in chunk_reader(f):
                hashobj.update(chunk)
    return hashobj.digest()


def find_duplicates(filenames: List[str]) -> List[List[str]]:
    files_by_size = defaultdict(list)
    files_by_small_hash = defaultdict(list)
    files_by_full_hash = defaultdict(list)

    for file in filenames:
        full_path = Path(file)
        try:
            file_size = full_path.stat().st_size
        except OSError:
            # not accessible (permissions, etc) - pass on
            continue
        files_by_size[file_size].append(full_path)

    # For all files with the same file size, get their hash on the first 1024 bytes
    for file_size, files in files_by_size.items():
        if len(files) < 2:
            continue  # this file size is unique, no need to spend cpu cycles on it

        for file in files:
            try:
                small_hash = get_hash(file, first_chunk_only=True)
            except OSError:
                # the file access might've changed till the exec point got here
                continue
            files_by_small_hash[(file_size, small_hash)].append(file)

    # For all files with the hash on the first 1024 bytes, get their hash on the full
    # file - collisions will be duplicates
    for files in files_by_small_hash.values():
        if len(files) < 2:
            continue  # the hash of the first 1k bytes is unique -> skip this file

        for file in files:
            try:
                full_hash = get_hash(file, first_chunk_only=False)
            except OSError:
                # the file access might've changed till the exec point got here
                continue

            files_by_full_hash[full_hash].append(str(file))

    return [v for v in files_by_full_hash.values() if len(v)]
