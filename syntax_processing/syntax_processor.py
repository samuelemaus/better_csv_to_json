import syntax_processing.syntax_constants as const
from json_conversion.csv_loader import RawCSVData
from json_conversion.json_creator import create_json_object
from json_conversion.json_schema import JsonSchemaElement, DEFAULT_TYPE_VALUES, ExclusionType
from syntax_processing import object_builder
from utils import to_camel_case


def process_csv_headings(raw_csv_data: RawCSVData):
    json_schema = {}
    first_row = raw_csv_data.values[0]
    elements = []
    for heading in raw_csv_data.headings:
        value = None
        extracted_heading, properties_substring, is_array = _parse_heading(heading)
        schema_element_args = {"is_array": is_array}
        if properties_substring is not None:
            properties = process_properties(properties_substring)

            if properties is not None and len(properties) > 0:
                for prop_key in properties.keys():
                    prop_value = properties[prop_key]
                    element_property_name = const.JSON_SCHEMA_ELEMENT_PROPERTIES_DICT[prop_key]
                    schema_element_args[element_property_name] = prop_value

        schema_element = _build_json_schema_element(heading, extracted_heading, first_row, schema_element_args)
        elements.append(schema_element)

    json_schema = object_builder.build_json_schema_object_hierarchy(elements)
    elements_dict = build_elements_dict(elements)
    return json_schema, elements_dict


def build_elements_dict(elements):
    elements_dict = {}
    for element in elements:
        if element.exclusion_type != ExclusionType.ALWAYS_EXCLUDE:
            elements_dict[element.original_name] = element
    return elements_dict


def _build_json_schema_element(original_heading, extracted_heading, first_row, schema_element_args):
    heading_name: str = original_heading if (len(schema_element_args) == 0) else extract_heading_name(original_heading)

    json_schema_element = JsonSchemaElement(original_heading, extracted_heading)
    for key in schema_element_args.keys():
        json_schema_element.__setattr__(key, schema_element_args[key])

    if json_schema_element.object_type is None:
        json_schema_element.object_type = _try_get_type_from_first_row(first_row[original_heading])

    if json_schema_element.default_value is None:
        json_schema_element.default_value = DEFAULT_TYPE_VALUES[json_schema_element.object_type]

    return json_schema_element


def extract_heading_name(heading):
    return heading


def _try_get_type_from_first_row(first_row_value: str):
    if first_row_value.isnumeric():
        return float if '.' in first_row_value else int
    if first_row_value.lower() == "true" or first_row_value.lower() == "false":
        return bool
    return str


def process_properties(properties_substring: str):
    properties = _get_unprocessed_properties(properties_substring)
    for key in properties.keys():
        value = properties[key]
        target_type = const.TYPE_PROPERTIES_DICT[key]
        converted_value = _convert_property_to_target_type(target_type, value)
        properties[key] = converted_value
    return properties


def _convert_property_to_target_type(target_type, value):
    if target_type == object:
        return value

    if target_type in const.TYPE_CONSTRUCTORS_DICT:
        func = const.TYPE_CONSTRUCTORS_DICT[target_type]
        val = func(value)
        return val

    return target_type(value)


def _parse_heading(heading: str):
    is_array = const.ARRAY_INDICATOR_KEY in heading

    if is_array:
        heading = heading.replace(const.ARRAY_INDICATOR_KEY, "")

    if "{" and "=" and "}" in heading:
        index_left = heading.rindex("{")
        index_right = heading.rindex("}")
        if index_left < index_right:
            equals_indexes = get_indexes_of_equal_signs(heading)
            if is_equality_assignment_between_braces(equals_indexes, index_left, index_right):
                extracted_heading = to_camel_case(heading[0:index_left])
                properties_substring = heading[index_left + 1: index_right].lower()
                return extracted_heading, properties_substring, is_array

    return to_camel_case(heading), None, is_array


def _get_unprocessed_properties(properties_substring: str):
    properties: dict = dict()
    properties_split = properties_substring.split(const.PROPERTIES_DELIMITER)
    for prop in properties_split:
        if const.EQUALS in prop:
            key, val = prop.split(const.EQUALS)
            properties[key] = val
            continue
        print("No assignment found in property: " + prop)
    return properties


def is_equality_assignment_between_braces(equals_indexes, index_left, index_right):
    for index in equals_indexes:
        equality_assignment_between_braces = index_left < index < index_right
        if equality_assignment_between_braces:
            return True
    return False


def get_indexes_of_equal_signs(heading):
    equals_indexes = []
    for index, char in enumerate(heading):
        if char is "=":
            equals_indexes.append(index)
    return equals_indexes
