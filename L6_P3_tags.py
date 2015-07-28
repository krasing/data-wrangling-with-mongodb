#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import codecs
import re
import json
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_tags(element, tags):
    for tag in element.iter('tag'):
        k = tag.attrib['k']
        v = tag.attrib['v']
        tags[k].add(v)
    return tags


def process_map(filename):
    tags = defaultdict(set)
    with codecs.open(filename, "r") as osm_file:
      for _, element in ET.iterparse(osm_file):
        tags = get_tags(element, tags)

    return tags


def test():

    tags = process_map('sample.osm')
    dtags = dict(tags)
    print repr(dtags).decode('unicode-escape')
    #pprint.pprint(repr(dtags).decode('unicode-escape'))
    #pprint.pprint(dtags)

    with codecs.open('tmp.txt', "w") as fo:
        fo.write(repr(dtags).decode('unicode-escape'))



if __name__ == "__main__":
    test()
