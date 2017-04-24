#!/bin/bash
virtualenv baseball_venv
source baseball_venv/bin/activate
pip install -r requirements.txt
python setup.py develop

cd baseball
python model.py
python get_data.py
python parse_data.py

rm -rf baseball_venv