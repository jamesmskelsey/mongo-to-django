from dataclasses import field


MAP = {
    "list": "array",
    "array": "array",
    "int": "integer",
    "bson.int64.Int64": "integer",
    "str": "string",
    "None": "null",
}

def translate_py_to_json(field_type):
    return MAP[field_type] if field_type is not None else ""