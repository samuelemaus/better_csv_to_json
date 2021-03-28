from collections import OrderedDict, deque, defaultdict

import syntax_processing.syntax_constants as const
from json_conversion.json_schema import JsonSchemaElement
from utils import to_camel_case, merge_dicts


def build_json_schema_object_hierarchy(schema_elements: []):
    final_schema = {}
    for element in schema_elements:
        if (not element.ignore_object_delimiter) and const.OBJECT_DELIMITER in element.original_name:
            delimited_heading: [] = element.original_name.split(const.OBJECT_DELIMITER)
            update_element_output_name_with_object_delimiter(delimited_heading, element)
            current_dict = defaultdict()
            build(current_dict, delimited_heading, element)
            merge_dicts(final_schema, current_dict)

        else:
            final_schema[element.output_name] = element.default_value
            element.json_key = element.output_name

    return final_schema


def update_element_output_name_with_object_delimiter(delimited_heading: [], element: JsonSchemaElement):
    output_name: str = ""
    for i, heading in enumerate(delimited_heading):
        output_name += to_camel_case(heading)
        if i < len(delimited_heading) - 1:
            output_name += const.OBJECT_DELIMITER

    element.output_name = output_name


def build(current_dict: defaultdict, headings: [], element: JsonSchemaElement):
    heading = to_camel_case(headings[0])
    if len(headings) > 1:
        next_dict = defaultdict()
        current_dict[heading] = next_dict
        sub_headings = headings[1:]
        build(next_dict, sub_headings, element)
    else:
        current_dict[heading] = element.default_value


