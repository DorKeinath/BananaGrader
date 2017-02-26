#!/usr/bin/env python
# import csv
import unicodecsv as csv
import json
import codecs
import io
from datetime import date

f = io.open('grades.json')
toCSV = json.load(f)
f.close()
keys = toCSV[0].keys()
csv_name = 'grades_' + str(date.today()) + '.csv'
with codecs.open(csv_name, 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(toCSV)
