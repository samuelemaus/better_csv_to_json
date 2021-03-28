import json
from json_conversion.json_schema import ExclusionType
import json_conversion.json_schema
from json_conversion.json_schema import JsonSchemaElement

# Heading Syntax designed to be case insensitive,
# all constants are lower-case and all passed-in values will be converted to lower.

# properties


TYPE_PROPERTY_KEY = "type"
DEFAULT_PROPERTY_KEY = "default"
EXCLUDE_PROPERTY_KEY = "exclude"
PRESERVE_CASE_PROPERTY_KEY = "preservecase"
IGNORE_OBJECT_DELIMITER_PROPERTY_KEY = "ignoreobjectdelimiter"

JSON_SCHEMA_ELEMENT_PROPERTIES_DICT = {
    TYPE_PROPERTY_KEY: "object_type",
    DEFAULT_PROPERTY_KEY: "default_value",
    EXCLUDE_PROPERTY_KEY: "exclusion_type",
    PRESERVE_CASE_PROPERTY_KEY: "preserve_case",
    IGNORE_OBJECT_DELIMITER_PROPERTY_KEY: "ignore_object_delimiter"
}

# type names
STRING_TYPE = "string"
INT_TYPE = "int"
FLOAT_TYPE = "float"
BOOLEAN_TYPE = "bool"
LITERAL_TYPE = "literal"

# misc
OBJECT_DELIMITER = "."
PROPERTIES_DELIMITER = ","
ARRAY_INDICATOR_KEY = "[,]"
EQUALS = "="
CSV_FILE_EXTENSION = ".csv"

# type dict
TYPE_PROPERTIES_DICT = {
    TYPE_PROPERTY_KEY: type,
    DEFAULT_PROPERTY_KEY: object,
    EXCLUDE_PROPERTY_KEY: ExclusionType,
    PRESERVE_CASE_PROPERTY_KEY: bool,
    IGNORE_OBJECT_DELIMITER_PROPERTY_KEY: bool,
    STRING_TYPE: str,
    INT_TYPE: int,
    FLOAT_TYPE: float,
    BOOLEAN_TYPE: bool,
    LITERAL_TYPE: json
}


def __get_type__(value: str):
    return TYPE_PROPERTIES_DICT[value]


TYPE_CONSTRUCTORS_DICT = {
    ExclusionType: json_conversion.json_schema.get_exclusion_type,
    type: __get_type__
}
