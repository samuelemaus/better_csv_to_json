from collections import OrderedDict, defaultdict
import syntax_processing.syntax_constants as const
from json_conversion import json_schema
from json_conversion.json_schema import ExclusionType
from json_conversion.csv_loader import RawCSVData
from utils import merge_dicts
import json


def create_json_object(raw_csv_data: RawCSVData, final_json_schema, schema_elements: {}):
    final_output = []
    for i, entry in enumerate(raw_csv_data.values):
        next_dict = {}
        merge_dicts(next_dict, final_json_schema)
        populate_schema(entry, next_dict, schema_elements)
        final_output.append(next_dict)

    return final_output


def populate_schema(row: OrderedDict, final_json_schema, schema_elements: {}):
    for key, value in row.items():
        schema_element = schema_elements[key]
        set_dict_value(final_json_schema, schema_element.output_name, value)


def set_dict_value(target_dict: defaultdict, location: str, value):
    if const.OBJECT_DELIMITER in location:
        split_locations = location.split(const.OBJECT_DELIMITER)
        nested_dict = get_nested_dict(target_dict, split_locations)
        nested_dict[split_locations[(len(split_locations) - 1)]] = value
        return
    target_dict[location] = value


def get_nested_dict(target_dict: defaultdict, split_locations: []):
    if len(split_locations) > 1:
        next_dict = target_dict[split_locations[0]]
        split_locations = split_locations[1:]
        return get_nested_dict(next_dict, split_locations)

    return target_dict
