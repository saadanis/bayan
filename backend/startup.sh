#!/bin/sh
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt --no-cache-dir
export FLASK_APP=./index.py
flask run -p 8000