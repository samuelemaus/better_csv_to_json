from enum import Enum


class ExclusionType(Enum):
    NEVER_EXCLUDE = 0
    EXCLUDE_IF_EMPTY = 1
    ALWAYS_EXCLUDE = 2


EXCLUDE_ALWAYS_KEY = "always"
EXCLUDE_IF_EMPTY_KEY = "ifempty"
EXCLUDE_NEVER_KEY = "never"

EXCLUSION_TYPE_DICT = {
    EXCLUDE_IF_EMPTY_KEY: ExclusionType.EXCLUDE_IF_EMPTY,
    EXCLUDE_ALWAYS_KEY: ExclusionType.ALWAYS_EXCLUDE,
    EXCLUDE_NEVER_KEY: ExclusionType.NEVER_EXCLUDE
}


def get_exclusion_type(value: str):
    return EXCLUSION_TYPE_DICT[value]


__DEFAULT_TYPE_VALUES__ = {
    str: "",
    float: 0,
    bool: False
}


class JsonSchemaElement:

    def __init__(self, original_name: str, output_name: str):
        self.original_name = original_name
        self.output_name = output_name

    original_name: str
    output_name: str
    object_type: type = None
    exclusion_type: ExclusionType = ExclusionType.NEVER_EXCLUDE
    ignore_object_delimiter: bool = False
    preserve_case: bool = False
    default_value: object = None
    is_array: bool = False
    json_key: str = ""
