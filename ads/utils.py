import csv
import json
from ads import models


def csv_to_json(csvfilepath, jsonfilepath):
    """
    This is our display of wit and cunning
    """
    jsonarray = []

    # read csv file
    with open(csvfilepath, encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csvreader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvreader:
            # add this python dict to json array
            jsonarray.append(row)

    # convert python jsonarray to JSON String and write to file
    with open(jsonfilepath, 'w', encoding='utf-8') as jsonf:
        jsonstring = json.dumps(jsonarray, indent=4)
        jsonf.write(jsonstring)


if __name__ == '__main__':
    csv_to_json('../datasets/ads.csv', '../datasets/ads.json')
    csv_to_json('../datasets/categories.csv', '../datasets/categories.json')
