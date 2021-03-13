import json
import jsonschema
from enum import Enum

OBJECT_KEY = "[:]"
ARRAY_KEY = "[,]"
IGNORE_IF_EMPTY_KEY = "(!)"
IGNORE_ALWAYS_KEY = "(~)"
DEFAULT_KEY = "{Default"
OBJECT_DELIMITER = ":"
ARRAY_DELIMITER = ","


class JsonType(Enum):
    INT = 0
    OBJECT = 1
    ARRAY = 2
    STRING = 3


JSON_TYPE_CONVERSION_DICT = {
    JsonType.INT: type(int),
    JsonType.OBJECT: type(object),
    JsonType.ARRAY: type([]),
    JsonType.STRING: type(str)
}


def get_type(value: str):
    if value.isnumeric():
        return JsonType.INT
    if value.__contains__(OBJECT_KEY):
        return JsonType.OBJECT
    if value.__contains__(ARRAY_KEY):
        return JsonType.ARRAY
    return JsonType.STRING


def get_default_value(name: str, value):
    if name.__contains__(DEFAULT_KEY):
        trimmed_default = name.replace("{", "")
        trimmed_default = trimmed_default.replace("}", "")
        default_value = trimmed_default.split('=')[1]
        return default_value
    return None


def get_json_value(name: str, value, json_type: JsonType):
    default_value = get_default_value(name, value)
    if default_value is not None:
        return default_value


def get_json_schema_element(name: str, value):
    if name.endswith(IGNORE_ALWAYS_KEY):
        return None
    return JsonSchemaElement(name, value)


def convert_value_to_type(value: str, json_type: JsonType):
    _type: type = JSON_TYPE_CONVERSION_DICT.get(json_type)

    if json_type == JsonType.ARRAY:
        converted_value = []
        split = value.split(ARRAY_DELIMITER)
        i = 0
        sub_type: JsonType = JsonType.OBJECT
        for val in split:
            if i == 0:
                sub_type = get_type(val)

            converted_entry_value = convert_value_to_type(val, sub_type)
            converted_value.append(converted_entry_value)
        return converted_value

    if json_type == JsonType.OBJECT:
        converted_value = {}
        split = value.split(OBJECT_DELIMITER)
        i = 0
        sub_type: JsonType = JsonType.OBJECT
        for val in split:
            if i == 0:
                sub_type = get_type(val)
            converted_value_entry = convert_value_to_type(val, sub_type)

    converted_value = _type(value)
    return converted_value


class JsonSchemaElement:

    def __init__(self, name: str, value):
        self.name = name
        self.default_value = get_default_value(name, value)
        if value == '' and self.default_value is not None:
            value = self.default_value

        self.object_type = get_type(value)
        if self.default_value is not None:
            self.default_value = convert_value_to_type(str(self.default_value), self.object_type)

        self.ignore_if_empty = name.endswith(IGNORE_IF_EMPTY_KEY)

    name: str
    object_type: JsonType
    default_value: object = None
    ignore_if_empty: bool = False
