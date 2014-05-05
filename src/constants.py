import os
import settings

__author__ = 'karl'

raw_xml_folder = os.path.join(settings.data_dir, "rawxml")

try:
    os.makedirs(raw_xml_folder)
except OSError:
    print("raw_xml_folder already exists")