import csv
import json
from inspect import signature

from json_conversion.json_creator import create_json_object
from json_conversion.json_schema import JsonSchemaElement
from jsonschema import validate
from json_conversion.csv_loader import RawCSVData
from json_conversion import csv_loader
from syntax_processing import syntax_processor
from enum import Enum


class DataType(Enum):
    CSV = 0
    JSON = 1


class CasingType(Enum):
    CAMEL_CASE = 0
    LOWER = 1
    UPPER = 2
    PRESERVE = 3


class ConversionParameters:
    evaluate_heading_syntax: bool = True
    casing_type: CasingType


def __load_json_data(file_name: str):
    with open(file_name) as f:
        data = json.load(f)
        return data


def _convert_csv_to_json(input_data: RawCSVData, params):
    output_json_schema, schema_elements = syntax_processor.process_csv_headings(input_data)
    output_json_object = create_json_object(input_data, output_json_schema, schema_elements)
    json_str = json.dumps(output_json_object)
    return json_str

def _convert_json_to_csv(input_data: json, params):
    return None


def __get_file_loader__(file_extension: str):
    file_loader_functions = {
        ".csv": csv_loader.load_csv_file,
        ".json": __load_json_data
    }

    if file_extension in file_loader_functions:
        return file_loader_functions[file_extension]
    return None


def __get_conversion_function(data_type: DataType):
    target_type_converter_functions = {
        DataType.JSON: _convert_csv_to_json,
        DataType.CSV: _convert_json_to_csv
    }

    if data_type in target_type_converter_functions:
        return target_type_converter_functions[data_type]
    return None


def convert_data(target_type: DataType, file_name: str, params: ConversionParameters):
    extension_index: int = file_name.rindex(".")
    extension = file_name[extension_index:file_name.__len__()]
    func = __get_file_loader__(extension)

    data = func(file_name)

    conversion_function = __get_conversion_function(target_type)
    if conversion_function is not None:
        return conversion_function(data, params)

    return None
