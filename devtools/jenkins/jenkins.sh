#!/bin/bash
virtualenv baseball_venv
source baseball_ven/bin/activate
pip install -r requirements.txt
python setup.py develop

cd baseball
python get_data.py
python parse_data.py

rm -rf baseball