import csv
import argparse
import pathlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('primary', type=pathlib.Path)
    parser.add_argument('sublist', type=pathlib.Path)
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--sort', action='store_true')

    args = parser.parse_args()
    new_list = {}
    with open(args.primary, newline='') as f:
        primary_list = csv.DictReader(f)
        fieldnames = primary_list.fieldnames
        for row in primary_list:
            new_list[(row['Name'], row['Street'])] = row
    new_row_count = 0
    update_row_count = 0
    with open(args.sublist, newline='') as f:
        sub_list = csv.DictReader(f)
        for row in sub_list:
            if (row['Name'], row['Street']) not in new_list:
                new_list[(row['Name'], row['Street'])] = row
                new_row_count += 1
            elif args.update:
                new_list[(row['Name'],
                          row['Street'])]['Comments'] = row['Comments']
                update_row_count += 1

    if args.sort:

        def sorter(entry):
            v = entry[1]
            return v['State'], v['City'], v['Name']

        new_list = {k: v for k, v in sorted(new_list.items(), key=sorter)}

    with open(args.primary, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for name, row in new_list.items():
            writer.writerow(row)

    print(f'Added {new_row_count} row(s)')
    if args.update:
        print(f'Updated {update_row_count} row(s)')


if __name__ == '__main__':
    main()
