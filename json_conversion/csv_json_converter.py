import csv
import json
from json_conversion.json_schema import JsonSchemaElement
from json_conversion.json_schema import JsonType
from json_conversion.json_schema import get_json_schema_element
from jsonschema import validate
from enum import Enum


def is_csv_file(file_name):
    return file_name.endswith("csv")


def get_json_schema(fieldnames, first_row):
    schema = []
    for key in fieldnames:
        schema_element: JsonSchemaElement
        schema_element = get_json_schema_element(key, first_row.get(key))
        if schema_element is not None:
            schema.append(schema_element)
    return schema


def process_row(row, fieldnames, schema):
    entry = {}

    for element in schema:
        doSomething = 0

    return entry


def load_csv_file(file_name):
    objects = []
    with open(file_name, encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        index = 0
        schema = []

        for row in reader:
            if index == 0:
                schema = get_json_schema(reader.fieldnames, row)

            entry = process_row(row, reader.fieldnames, schema)
            objects.append(entry)
            index += 1

    return objects


def convert_to_json(csv_reader, json_schema):
    return None


def convert_file(file_name):
    if is_csv_file(file_name):
        print("yep, that's a csv alright")
        reader = load_csv_file(file_name)
        # schema = get_json_schema(reader)
        # convert_to_json(reader, schema)

    else:
        print("Input file is not a .csv file.")
