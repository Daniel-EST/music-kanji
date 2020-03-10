import csv


def parse_csv(csv_string):
    data = list(csv.reader(csv_string.split('\n')))
    labels = data[0]
    rows = data[1:]

    for row in rows:
        if len(row) > 0:
            yield dict(zip(labels, row))
