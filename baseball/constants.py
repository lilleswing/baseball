import os
import baseball.settings as settings

__author__ = 'karl'

raw_xml_folder = os.path.join(settings.data_dir, "rawxml")
base_scrape_url = "http://gd2.mlb.com/components/game/mlb"

batch_size = 1000
BATTER = "batter"
PITCHER = "pitcher"

try:
    os.makedirs(raw_xml_folder)
except OSError:
    print("raw_xml_folder already exists")
