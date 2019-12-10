#!/usr/bin/env bash

python3 -m venv venv
source venv/bin/activate
pip install -r zappa_project/requirements.txt
zappa deploy dev