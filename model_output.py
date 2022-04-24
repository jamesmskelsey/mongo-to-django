import xlsxwriter

def model_to_xlsx(model_name: str, data: dict) -> bool:
  workbook = xlsxwriter.Workbook('database.xlsx')
  worksheet = workbook.add_worksheet(model_name)
  bold_format = workbook.add_format()
  bold_format.set_bold()
  
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
    col += 2

  row = 1
  col = 0
  # 2. For each field, write the field name, then...
  for field_name, field_types in data.items():
    worksheet.write(row, col, field_name)
    ## 2a. For each type in each field, write the type, then in the next column write the number
    for type_name, count_of_type in field_types.items():
      col += 1
      worksheet.write_string(row, col, extract_class_name(type_name))
      col += 1
      worksheet.write_number(row, col, count_of_type)
    row += 1
    col = 0



  # # Write a total using a formula.
  # worksheet.write(row, 0, 'Total')
  # worksheet.write(row, 1, '=SUM(B1:B4)')

  workbook.close()

  return True

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