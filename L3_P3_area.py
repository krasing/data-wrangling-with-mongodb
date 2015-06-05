#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

def get_type(item):
    item = item.strip()
    if item == 'NULL':
        return type(None)
    if item[0]=='{':
        return type([])
    try:
        float(item)
        return type(1.1)
    except ValueError:
        return type('')

def fix_area(area):

    # YOUR CODE HERE
    area = area.strip()
    input_type = get_type(area)
    if input_type == type(None):
        return None
    if input_type == type(1.1):
        area = float(area)
    if input_type == type(''):
        area = None
    if input_type == type([]):
        area = area[1:-1]
        areaList = area.split('|')
        number_length = 0
        area == None
        for number in areaList:
            if get_type(number)==type(1.1):
                if len(number)>number_length:
                    area = float(number)
                    number_length = len(number)
    return area




def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[8]["areaLand"] == 55166700.0
    assert data[3]["areaLand"] == None


if __name__ == "__main__":
    test()