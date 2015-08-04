#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import codecs
import re
import json
"""
Auditing the dataset
"""

postcode_re = re.compile(r'^[12]\d{3}$', re.IGNORECASE)
street_type_re = re.compile(ur'^\b\S+\s*\.?\s', re.IGNORECASE | re.U)

expected_street = [u'ул. ', u'бул. ', u'пл. ']

lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(ur'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]', re.U)
problemchars2 = re.compile(ur'[\\]', re.U)
quoteproblem = re.compile(ur'&.*?;')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]



class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


def get_postcode_tags(element, tags):
    # get a set of postcodes that are not four digit numbers starting with 1 or 2
    for tag in element.iter('tag'):
        k = tag.attrib['k']
        v = tag.attrib['v']
        if k=='addr:postcode' or k == 'postal_code':
            m = postcode_re.match(v)
            if not m:
                tags[k].add(v)
    return tags
    
    
def is_street_name(elem):
    k = elem.attrib['k']
    return (k == "addr:street")
    
def is_postcode(elem):
    k = elem.attrib['k']
    out = k == "addr:postcode" or k == "postal_code"
    return out
    
def is_phonenum(elem):
    k = elem.attrib['k']
    out = k == "contact:phone" or k == "phone"
    return out
    
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street:
            street_types[street_type].add(street_name)
    return 
            
def audit_postcode(postcodes, text):
    m = postcode_re.match(text)
    if not m:
        if text in postcodes.keys():
            postcodes[text] += 1
        else:
            postcodes[text] = 1
            
def strip_phone(text):
    number_as_list = re.findall(r'\d+', text)
    
    if number_as_list[0][0:2] == '00':
        number_as_list[0] = number_as_list[0][2:]
        if len(number_as_list[0])==0:
            number_as_list = number_as_list[1:]
    if number_as_list[0] == '359':
        number_as_list = number_as_list[1:]
    elif number_as_list[0][0:3] == '359':
        number_as_list[0] = number_as_list[0][3:]
        
    if number_as_list[0][0] != '0':
        number_as_list[0] = '0' + number_as_list[0]   
        
    number = ''.join(number_as_list)
    
    return number
    
def split_phone(text):
    codes = ['02', '087', '088', '089']
    code = ''
    index = 0
    for c in codes:
        if text.startswith(c):
            code = c
            index = len(c)
            continue
    local = text[index:]
    
    return code, local
    
def audit_phone(text):
    number_string = strip_phone(text)
    (code, local) = split_phone(number_string)
    if len(code) == 0 or len(local) != 7:
        print text
        return None
    return code, local
    
def is_bad_street_type(street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street:
            return True
        else:
            return False 
    else:
        return True

def improve_street_name(text):
    isBlvd = text[-4:]== u'шосе'
    isStr1 = text[:3] == u'ул.'
    isStr2 = text[:6] == u'улица '
    if isBlvd:
        better = u'бул. ' + text
    elif isStr1:
        better = u'ул. ' + text[3:]
    elif isStr2:
        better = u'ул. ' + text[6:]
    elif re.search('[a-z]', text):
        better = text
    else:
        better = u'ул. ' + text
    return better

def get_amenity(element, tags):
    for tag in element.iter('tag'):
        k = tag.attrib['k']
        v = tag.attrib['v']
        if k=='amenity':# and v == 'yes':
            tags[k].add(v)
    return tags


def shape_element(element):
    # clean and reshape element
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node["created"] = {}
        if element.tag == "node":
            node["pos"] = [0., 0.]
            node["type"] = "node"
        if element.tag == "way":
            node["node_refs"] = []
            node["type"] = "way"
        for key,value in element.attrib.items():
#            if quoteproblem.search(value):
#                quoteproblem.sub('', value)
#                print value
            if key in CREATED:
                node["created"][key] = value
            elif key == 'lat':
                node["pos"][0] = float(value)
            elif key == 'lon':
                node["pos"][1] = float(value)
            else:
                node[key] = value
        for tag in element.iter('tag'):
            kvalue = tag.attrib['k']
            value = tag.attrib['v']
            if problemchars.search(kvalue):
                continue
            if problemchars2.search(value):
                continue
#            if quoteproblem.search(value):
#                quoteproblem.sub('', value)
#                print value
            
            if is_phonenum(tag):
                number_string = strip_phone(value)
                (code, local) = split_phone(number_string)
                if 'phone' not in node.keys():
                    node['phone'] = {}
                node['phone']['full'] = value
                if len(local) == 7:
                    node['phone']['local'] = local
                    if len(code) == 0:
                        node['phone']['code'] = '02'
                    else:
                        node['phone']['code'] = code
                
            
            elif lower_colon.match(kvalue):
                composed = re.split(':',kvalue)
                if len(composed)==2 and composed[0]=='addr':
                    address_fiels = composed[1]
                    if 'address' not in node.keys():
                        node['address'] = {}
                    if composed[1] == 'street':
                        if is_bad_street_type(value):
                            value = improve_street_name(value)
                    node['address'][address_fiels] = value  
                elif composed[0]!='addr':
                    node[kvalue] = value
            else:
                node[kvalue] = value

        for nd in element.iter('nd'):
            ref = nd.attrib['ref']
            node["node_refs"].append(ref)
    
        
        return node
    else:
        return None

def audit_map(filename, pretty = False):
    postcodes = {}
    street_types = defaultdict(set)
    
    # audit dataset
    with codecs.open(filename, "r") as osm_file:
        for _, elem in ET.iterparse(osm_file):
            if elem.tag == "node" or elem.tag == "way":
                # audit street names                
                for tag in elem.iter("tag"):
                    if is_street_name(tag):
                        audit_street_type(street_types, tag.attrib['v'])
                    if is_postcode(tag):
                        audit_postcode(postcodes, tag.attrib['v'])
                    if is_phonenum(tag):
                        v = tag.attrib['v']
                        audit_phone(v)
                 
    return postcodes, street_types

def process_map(filename, pretty = False):
                 
    # clean and reshape dataset
    file_out = "{0}.json".format(filename)
    i = 0

    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(filename):
            el = shape_element(element)
            if el:
                print i
                i += 1
                if pretty:
                    fo.write(json.dumps(el, indent=2).decode('unicode-escape') +"\n")
                else:
                    fo.write(json.dumps(el, ensure_ascii=True).decode('unicode-escape') + "\n")

def test():

    (postcodes, street_types) = audit_map('sample.osm')
    postcodesd = dict(postcodes)
    
    print 'Inconsistent Post codes:'
    MyPrettyPrinter().pprint(postcodesd)
    print
    print 'Unexpected street types:'
    MyPrettyPrinter().pprint(dict(street_types))
    
    process_map('sofia_bulgaria.osm')
    #process_map('sample.osm')


if __name__ == "__main__":
    test()
