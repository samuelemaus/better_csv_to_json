from collections import OrderedDict, defaultdict
import syntax_processing.syntax_constants as const
from json_conversion import json_schema
from json_conversion.json_schema import ExclusionType, JsonSchemaElement
from json_conversion.csv_loader import RawCSVData
from syntax_processing.array_builder import build_array
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


def populate_schema(row: OrderedDict, json_object: {}, schema_elements: {}):
    for key, value in row.items():
        if key in schema_elements:
            schema_element = schema_elements[key]

            if schema_element.exclusion_type == ExclusionType.EXCLUDE_IF_EMPTY and value == "":
                process_local_exclusion(json_object, schema_element)
                continue

            final_value = get_final_value(value, schema_element)
            set_dict_value(json_object, schema_element.output_name, final_value)


def process_local_exclusion(json_object: {}, schema_element: JsonSchemaElement):
    if const.OBJECT_DELIMITER in schema_element.output_name:
        split_locations = schema_element.output_name.split(const.OBJECT_DELIMITER)
        nested = get_nested_dict(json_object, split_locations)
        del nested[split_locations[(len(split_locations) - 1)]]
        return

    del json_object[schema_element.output_name]


def get_final_value(value, schema_element: JsonSchemaElement):
    if value == "":
        return schema_element.default_value

    if schema_element.is_array:
        return build_array(value, schema_element.object_type)

    converted = schema_element.object_type(value)
    return converted


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
