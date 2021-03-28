from json_conversion import data_converter
from json_conversion import csv_loader

# converter = csv_json_converter

fileName1 = "resources/people.csv"

data = data_converter.convert_data(data_converter.DataType.JSON, fileName1, None)

print(data)
