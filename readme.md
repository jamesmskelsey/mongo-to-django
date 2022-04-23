# What it is

This program will iterate by 1000 documents across a mongo database collection and return a list 
of all of the fields, with the types of data in the fields.

This is meant to be very similar to the MongoDBCompass "Analyze" feature, except that the user
can look at the entire collection.

## Usage
1. Enter connection string for your Mongo database in the .env file as CONNECTION_STRING.
2. Enter your database name, and the collection you wish to analyze.
3. Run `py mtd.py`

## Next Steps
* Analyze any number of collections given in the .env file.
* Output data to CSV or XLS file.
* XLS file gets data on sheet two, sheet one contains charts to help the user consume the data.
* An option to create Django models based on validated data in the XLS file. i.e. the program
returns a dataset, the user reviews the data, and then marks the correct type of data for each column
and then the models can be generated based on that.
* Based on column name and the types of data, make appropriate suggestions about what type a column 
should be.

