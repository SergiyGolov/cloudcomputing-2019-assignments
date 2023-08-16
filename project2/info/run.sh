#!/usr/bin/env bash

export FLASK_APP=server.py
export DB_HOST=35.195.138.219
export DB_PORT=3306
export DB_DBNAME=watches
export DB_USER=watches
export DB_PASS=watches
export HTTP_USER=cloud
export HTTP_PASS=computing

flask run --port=1080