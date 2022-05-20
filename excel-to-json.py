"""
Database (.xlsx) to Pydantic model. Assumes the data you want 
to convert is correctly formatted in database.xlsx.

Will take the "Field Name" and "Type" columns on the far left
from database.xlsx 
"""
from dataclasses import field
import json
from openpyxl import load_workbook
from py_to_json import translate_py_to_json

# Open the file


wb = load_workbook(filename="database.xlsx")

print(wb.sheetnames)

def model_file_name(model_name):
    model_name = model_name.lower()
    return f"{model_name}.json"

def capitalize_first(name):
    lower = name.lower()
    return f"{lower[0:1]}{lower[1:]}"

for sheetname in wb.sheetnames:
    ws = wb[sheetname]
    model_as_dict = {}
    for row in ws.values:
        # read the pairs and create a dictionary to make it easy to work with
        field_name = row[0]
        field_type = row[1]
        if field_name != 'Field Name' and field_name != '_id':
            model_as_dict[field_name] = field_type

    schema = {
        "$id": model_file_name(sheetname),
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": capitalize_first(sheetname),
        "type": "object",
        "properties": {

        },
        "required": [

        ],
        "definitions": {

        }
    }

    d = {
        "name": "str",
        "name.first": "str",
        "name.last": "str",
    }

    only_primary_fields = [(e, v) for (e,v) in model_as_dict.items() if "." not in str(e)]
    for field_name, field_type in only_primary_fields:
        if field_name != "null":
            schema['properties'][field_name] = {
                "type": translate_py_to_json(field_type),
                "description": "Replace me."
            }

    # Create a .py file, make the model
    with open(model_file_name(sheetname), 'w', encoding='utf-8') as f:
        f.write(json.dumps(schema, indent=4))
        f.close()
        # level = 0
        # f.write(indent(level, "{\n"))
        # level += 1
        # f.write(indent(level, f'"$id": "{sheetname}.json",\n'))
        # f.write(indent(level, f'"$schema": "http://json-schema.org/draft-07/schema#",\n'))
        # f.write(indent(level, f'"title": "{capitalize_first(sheetname)}",\n'))
        # f.write(indent(level, f'"type": "object",\n'))
        # # properties
        # f.write(indent(level, '"properties": {\n'))
        # # logic to write all of the fields at indent 2 and beyond

        # for field_name, field_type in model_as_dict.items():
        #     write_property(f, level, field_name, field_type)

        # f.write(indent(level, '},\n'))

        # # A blank space for required fields so the user can fill it in
        # f.write(indent(level, '"required": [\n'))
        # f.write(indent(level, '],\n'))

        # # then we fill in the definitions of things like "Pet", etc
        # f.write(indent(level, '"definitions": {\n'))
        # # logic to write all of the different properties of the sub models
        # f.write(indent(level, '}\n'))


        # level -= 1
        # f.write(indent(level, "}\n"))
        # f.close()

