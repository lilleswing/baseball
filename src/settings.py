import os
__author__ = 'karl'

#Production
database_url = 'postgresql://postgres:NaClH2O@localhost:5432/baseball'
database_echo = True
raw_xml_folder = "/home/leswing/Downloads/rawxml"

#Dev
#database_url = 'sqlite:////Users/karl/Documents/CompSci/baseball/src/foo.db'
#database_echo = True
#raw_xml_folder = "scraper/rawxml"

try:
    os.makedirs(raw_xml_folder)
except OSError:
    print("raw_xml_folder already exists")
