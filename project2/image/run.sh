#!/usr/bin/env bash

export FLASK_APP=server.py
export HTTP_USER=cloud
export HTTP_PASS=computing

flask run --port=1080