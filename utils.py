def to_camel_case(value: str):
    first = value[0].lower()
    rest = value[1:]
    if rest[0:1].isupper():
        rest = to_camel_case(rest)
    return first + rest


def merge_dicts(source_dict: {}, new_dict: {}):
    for key, value in new_dict.items():
        if key in source_dict:
            merge_dicts(source_dict[key], value)
        else:
            source_dict[key] = value
