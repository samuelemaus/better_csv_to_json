import csv
from collections import OrderedDict

from json_conversion.json_schema import JsonSchemaElement


class RawCSVData:
    headings: []
    values: OrderedDict

    def __init__(self, headings, values):
        self.headings = headings
        self.values = values


def is_csv_file(file_name):
    return file_name.endswith("csv")


def get_keys(heading_row):
    keys = []
    for heading in heading_row:
        keys.append(heading)
    return keys


def load_csv_file(file_name):
    headings = []
    objects = []
    with open(file_name, encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)

        headings = reader.fieldnames

        for row in reader:
            objects.append(row)

    return RawCSVData(headings, objects)
