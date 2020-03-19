import re
import sys

HTML_SUBST = [(r'&quot;', r'"'),
              (r'&nbsp;', r' '),
              (r'&amp;', r'&')]


def clean_diary_entry(diary_entry: list):
    entry = '\n'.join(diary_entry).strip('\n')
    for html, subst in HTML_SUBST:
        entry = re.sub(html, subst, entry)
    return entry


def entries_by_date(fname):
    diary_entries = []
    diary_date = None
    diary_entry = []
    lines = fname.read().splitlines(keepends=False)
    for line in lines:
        if re.match(r'\d{4}-\d\d-\d\d', line) is not None:
            if diary_date is not None:
                diary_entries.append((diary_date, clean_diary_entry(diary_entry)))
            diary_date = line
            diary_entry = []
        else:
            diary_entry.append(line)

    if diary_date is not None:
        diary_entries.append((diary_date, clean_diary_entry(diary_entry)))
    return diary_entries


def main(diary_filename):
    with open(diary_filename) as diary_file:
        for ofname, oftext in entries_by_date(diary_file):
            with open(f'{ofname}.txt', 'wt') as out:
                out.write(oftext)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'Usage: {sys.argv[0]} diary_name.txt [diary_name.txt [...]]')
        exit(1)
    for fname in sys.argv[1:]:
        main(fname)
