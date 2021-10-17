import os
import io


def last_lines(filename: str):
    with open(filename, 'rb') as fh:
        reserve = b''
        fh.seek(0, os.SEEK_END)
        file_remaining = fh.tell()
        while file_remaining > 0:
            next_block_size = min(file_remaining, io.DEFAULT_BUFFER_SIZE)
            file_remaining -= next_block_size
            fh.seek(file_remaining)
            buffer = fh.read(next_block_size) + reserve
            lines = buffer.splitlines(keepends=True)
            reserve = lines.pop(0)
            yield from [line.decode() for line in lines[::-1]]
        if reserve != b'':
            yield reserve.decode()
