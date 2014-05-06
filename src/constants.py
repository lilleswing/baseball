import os
import settings

__author__ = 'karl'

raw_xml_folder = os.path.join(settings.data_dir, "rawxml")
raw_matrix_folder = os.path.join(settings.data_dir, "rawmatrix")
base_scrape_url = "http://gd2.mlb.com/components/game/mlb"

raw_xml_folder = os.path.join(settings.data_dir, "rawxml")
try:
    os.makedirs(raw_xml_folder)
except OSError:
    print("raw_xml_folder already exists")

try:
    os.makedirs(raw_matrix_folder)
except OSError:
    print("raw_matrix_folder already exists")
