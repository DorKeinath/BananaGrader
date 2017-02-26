#!/usr/bin/env python
import codecs
import csv
import json

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

with codecs.open('students.csv', encoding='utf-8') as f:
    reader = unicode_csv_reader(f)
    keys = [k.strip() for k in reader.next()]
    result = []
    for row in reader:
        d=dict(zip(keys, row))
        result.append(d)

    for d in result:
        for k, v in d.iteritems():
            print k, v
    print result
    with open('students.json', 'w') as f:
        json.dump(result,f)

    ## So wird es haesslich gespeichert
    # with open('students.json', 'w') as file_:
    #     file_.write(str(result))
