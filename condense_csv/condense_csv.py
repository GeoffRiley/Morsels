import csv
import io
from collections import defaultdict


def condense_csv(text: str, id_name: str = None) -> str:
    dialect = csv.Sniffer().sniff(text)
    headers = ['ID', 'attribute name', 'attribute value'] if id_name else None

    table = csv.DictReader(text.splitlines(), headers, dialect=dialect)
    if not id_name:
        headers = [field for field in table.fieldnames]
        id_name = headers[0]

    results = {}
    out_headers = [id_name]
    for row in table:
        id, param1, param2 = [row[h] for h in headers]
        if id not in results:
            results[id] = defaultdict(str)
            results[id][id_name] = id
        if param1 not in out_headers:
            out_headers.append(param1)
        results[id][param1] = param2

    out = io.StringIO()
    write_out = csv.DictWriter(out, out_headers, dialect=dialect)
    write_out.writeheader()
    write_out.writerows(iter(results.values()))

    output = out.getvalue()
    out.close()

    return output
