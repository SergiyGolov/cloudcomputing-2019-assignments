#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
import os

app = Flask(__name__)


@app.route('/<path:path>')
def home(path):
    output = "/"
    output += path+"<br/>"

    args = [k+": "+request.args[k] for k, v in request.args.items()]
    output += "<br/>".join(args)

    env = [k+"="+os.environ[k] for k, v in os.environ.items()]
    output += "<br/><br/>Env:<br/>"+"<br/>".join(env)

    return output


if __name__ == '__main__':
    app.run(port=5000, debug=False, host='0.0.0.0')
