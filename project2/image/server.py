#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, request, send_file
import urllib3
from io import BytesIO


api_image_v1_prefix = '/image/v1'

http = urllib3.PoolManager()
app = Flask(__name__)

@app.route(f'{api_image_v1_prefix}/', methods=['GET'])
def home():
    return jsonify("Health check hello.")


@app.route(f'{api_image_v1_prefix}/watch/<sku>', methods=['GET'])
def get_image(sku):
    request = http.request('GET',f'https://s3-eu-west-1.amazonaws.com/cloudcomputing-2018/project1/images/{sku}.png')
    
    if request.status != 200:
        abort(404)
    
    img = BytesIO(request.data)

    return send_file(img, mimetype='image/png')


@app.after_request
def add_header(response):
    response.direct_passthrough = False 
    # Headers to allow GET data to be valid 1 hour
    response.cache_control.max_age = 3600
    response.cache_control.public = True
    response.add_etag()

    # Headers for testing with swagger
    response.headers.add('Access-Control-Allow-Origin',
                         'https://editor.swagger.io')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, api_key, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, DELETE, PUT, PATCH, OPTIONS')
    return response


if __name__ == '__main__':
    app.run(port=1080, debug=False, host='0.0.0.0')
