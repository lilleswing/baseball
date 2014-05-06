import os
import settings

__author__ = 'karl'

raw_xml_folder = os.path.join(settings.data_dir, "rawxml")
raw_matrix_folder = os.path.join(settings.data_dir, "rawmatrix")

try:
    os.makedirs(raw_xml_folder)
except OSError:
    print("raw_xml_folder already exists")

try:
    os.makedirs(raw_matrix_folder)
except OSError:
    print("raw_matrix_folder already exists")
