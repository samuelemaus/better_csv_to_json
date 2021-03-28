import syntax_processing.syntax_constants as const


def build_array(unprocessed_value: str, object_type: type):
    split = unprocessed_value.split(const.PROPERTIES_DELIMITER)
    arr = []
    for val in split:
        val = val.strip()
        arr.append(object_type(val))

    return arr
