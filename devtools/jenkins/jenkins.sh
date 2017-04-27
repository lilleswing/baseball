#!/bin/bash
virtualenv -p python3 baseball_venv
source baseball_venv/bin/activate
pip install -r requirements.txt
python setup.py develop

cd baseball
python model.py
python get_data.py
python parse_data.py

sqlite3 baseball.db .dump > ../baseball.bak
git add ../baseball.bak
git commit -m "Updating Baseball Database"

rm -rf ../baseball_venv
