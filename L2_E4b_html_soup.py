#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the approprate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
import requests
import json

html_page = "page_source.html"

s = requests.Session()
r = s.get('http://www.transtats.bts.gov/Data_Elements.aspx?Data=2')
soup = BeautifulSoup(r.text)
        # print soup.find_all('input')[:2]
eventvalidation_element = soup.find(id="__EVENTVALIDATION")
eventvalidation = eventvalidation_element["value"]
viewstate = soup.find(id="__VIEWSTATE")['value']
viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")['value']




r = s.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                data={'AirportList': "BOS",
                      'CarrierList': "VX",
                      'Submit': 'Submit',
                      "__EVENTTARGET": "",
                      "__EVENTARGUMENT": "",
                      "__EVENTVALIDATION": eventvalidation,
                      "__VIEWSTATE": viewstate,
                      "__VIEWSTATEGENERATOR": viewstategenerator
                })


f = open("VX_BOS.html", "w")
f.write(r.text)
f.close()