import os
__author__ = 'karl'

#Production
#database_url = 'postgresql://postgres:NaClH2O@localhost:3247/baseball', echo=True)
#database_echo = True
#raw_xml_folder = "scraper/rawxml"

#Dev
database_url = 'sqlite:////Users/karl/Documents/CompSci/baseball/src/foo.db'
database_echo = True
raw_xml_folder = "scraper/rawxml"

os.makedirs(raw_xml_folder)
