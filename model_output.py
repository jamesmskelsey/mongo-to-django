import xlsxwriter

def model_to_xlsx(model_name: str, data: dict) -> bool:
  workbook = xlsxwriter.Workbook(f'{model_name}.xlsx')
  worksheet = workbook.add_worksheet(model_name)
  bold_format = workbook.add_format()
  bold_format.set_bold()

  percentage_format = workbook.add_format({'num_format': '0.00%'})
  
  # Start from the first cell. Rows and columns are zero indexed.
  row = 0
  col = 0

  # 1. Write the column names at the top row
  worksheet.write(row, col, "Field Name", bold_format)
  col += 1

  ## 1a. Find the field with the most types, and write that many pairs of Type/Count on the top row
  longest = find_field_with_most_types(data)
  for _ in range(longest):
    worksheet.write(0, col,     "Type",  bold_format)
    worksheet.write(0, col + 1, "Count", bold_format)
    worksheet.write(0, col + 2, "Percent",     bold_format)
    worksheet.write(0, col + 3, " ",     bold_format)
    col += 4

  row = 1
  col = 0
  ## 1b. Analyze the fields and fill an array with objects representing what will end up being each row
  analyzed_fields = analyze_fields(data)
  print(analyzed_fields)
  
  number_of_items = 0
  # 2. For each field, write the field name, then...
  for field_name, field_types in data.items():
    worksheet.write(row, col, field_name)
    ## 2a. For each type in each field, write the type, then in the next column write the number
    # track how many items we listed, so we can include a "undefined" if not all of them are used
    count = 0
    if field_name == "_id":
      for _, count_of_type in field_types.items():
        number_of_items = count_of_type
    else:  
      for type_name, count_of_type in field_types.items():
        col += 1
        # Type of the field
        worksheet.write_string(row, col, extract_class_name(type_name))
        col += 1
        # How many are this type
        worksheet.write_number(row, col, count_of_type)
        count += count_of_type
        col += 1
        # Percentage of this type of the total
        worksheet.write_number(row, col, count_of_type / number_of_items, percentage_format)
        col += 1
      # in the last row, record an undefined column if they're not all accounted for
      if count < number_of_items:
        col += 1
        worksheet.write_string(row, col, "undefined")
        col += 1
        worksheet.write_number(row, col, number_of_items - count)
        col += 1
        worksheet.write_number(row, col, (number_of_items - count) / number_of_items, percentage_format)
        col += 1


    # Reset the cursor to the beginning of the next row for the next field
    row += 1
    col = 0



  # # Write a total using a formula.
  # worksheet.write(row, 0, 'Total')
  # worksheet.write(row, 1, '=SUM(B1:B4)')

  workbook.close()

  return True

def analyze_fields(data: dict) -> list:
  output = []
  number_of_items = 0
  for field_name, field_types in data.items():
    field = {
      "name": field_name,
      "types": [],
      "count": 0
    }
    if field_name == "_id":
      for _, count_of_type in field_types.items():
        number_of_items = count_of_type
    else:  
      for type_name, count_of_type in field_types.items():
        # Type of the field
        # How many are this type
        # Percentage of this type of the total
        type_obj = {
          "type": extract_class_name(type_name),
          "count": count_of_type,
          "percent": count_of_type / number_of_items,
        }
        field["count"] += count_of_type
        field["types"].append(type_obj)
      # in the last index, record an undefined column if they're not all accounted for
      if field["count"] < number_of_items:
        type_obj = {
          "type": "undefined",
          "count": number_of_items - field["count"],
          "percent": (number_of_items - field["count"]) / number_of_items
        }
    # Finally, append the field to the output of the analysis.
    output.append(field)
  return output

        

def find_field_with_most_types(data: dict) -> int:
  longest = 0
  for _, types in data.items():
    current = len(types.items())
    if current > longest:
      longest = current
  return longest

def extract_class_name(s: str) -> str:
  s = str(s)
  return s[s.find("'") + 1:s.rfind("'")]

# model_to_xlsx('companies', {
#   "_id": {"<class 'bson.objectid.ObjectId'>": 125342},
#   "address": {"<class 'dict'>": 125342},
#   "business_description": {"<class 'str'>": 122090, "<class 'NoneType'>": 3251, "<class 'bson.int64.Int64'>": 1},
#   "claimed_client": {"<class 'str'>": 85946},
#   "contact_email": {"<class 'str'>": 124425, "<class 'NoneType'>": 917},
#   "domain_name": {"<class 'str'>": 125342},
#   "executives": {"<class 'list'>": 97038, "<class 'NoneType'>": 28304},
#   "image_url": {"<class 'str'>": 116619, "<class 'NoneType'>": 8723},
#   "is_subsidiary": {"<class 'int'>": 21340, "<class 'float'>": 4},
#   "name": {"<class 'str'>": 125342},
#   "num_employees": {"<class 'int'>": 85107, "<class 'bson.int64.Int64'>": 11933, "<class 'str'>": 735, "<class 'float'>": 2, "<class 'NoneType'>": 27565},
# })