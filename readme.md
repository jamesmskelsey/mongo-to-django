# What it is

This program will iterate by 1000 documents across a mongo database collection and return a list 
of all of the fields, with the types of data in the fields.

This is meant to be very similar to the MongoDBCompass "Analyze" feature, except that the user
can look at the entire collection.

## Usage - Mongo to Excel
1. Enter connection string for your Mongo database in the .env file as CONNECTION_STRING.
2. Enter your database name, and the collection you wish to analyze.
3. Run `py mtd.py`

## Data to Pydantic
1. Ensure the field names and data types are in the left most column of `database.xlsx`
2. Run `py dtp.py`
3. Review the output pydantic model

Data is output to an XLS file currently just called "database.xlsx".
## Next Steps
* Analyze any number of collections given in the .env file.
* XLS file gets data on sheet two, sheet one contains charts to help the user consume the data.
* An option to create Django models based on validated data in the XLS file. i.e. the program
returns a dataset, the user reviews the data, and then marks the correct type of data for each column
and then the models can be generated based on that.
* Based on column name and the types of data, make appropriate suggestions about what type a column 
should be. Todo: make each data type into a array of dicts and pass it off to an analyzer first before 
writing it to the work sheet. That way each field turns in to this:

  ``` python
  field = [
    {
      "field_name": "example_name",
      "types": [
        {
          "type": "str",
          "count": 5215,
          "percent": 52.15,
          "format": green_format
        },
        {
          "type": "undefined",
          "count": 4785,
          "percent": 47.85,
          "format": red_format
        }
      ]
    }
  ]
  ```

## Completed Tasks
* :white_check_mark: Output data to XLS file.
* :white_check_mark: Add percentage column.
* :white_check_mark: Analyze one level of nested documents

### FAQ

1. Why did you use xlsxwriter for one thing, and then turn around and use openpyxl for the other?
A. My friend my friend! It's because I found the one thing, and then realized it couldn't do the other thing, so I wasn't going to go back and rewrite the first thing right away.