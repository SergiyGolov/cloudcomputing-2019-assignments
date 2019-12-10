#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from flask import Flask, abort, jsonify, request
    from flask_httpauth import HTTPBasicAuth
    from werkzeug.security import generate_password_hash, check_password_hash
    import os
    import boto3

    http_user = os.environ['HTTP_USER']
    http_pass = os.environ['HTTP_PASS']
    #http_user = 'cloud'
    #http_pass = 'computing'

    api_info_v2_prefix = '/info/v2'

    app = Flask(__name__)
    auth = HTTPBasicAuth()
except Exception as e:
    print("Failure with {}".format(e))

def get_connection():
    # works if aws configure in aws cli has been used
    return boto3.resource('dynamodb', region_name='eu-west-3')


@auth.verify_password
def verify_password(username, password):
    if username == http_user:
        return check_password_hash(generate_password_hash(http_pass), password)
    return False

@app.route(f'/', methods=['GET'])
def home():
    return jsonify("Health check hello.")


@app.route(f'{api_info_v2_prefix}/watch/<sku>', methods=['GET'])
@auth.login_required
def get_watch_data(sku):
    connection = get_connection()

    table = connection.Table('watches')

    try:
        response = table.get_item(Key={'sku': sku})
    except ClientError as e:
        print(e.response['Error']['Message'])
        abort(404)
    else:
        item = response['Item']
        item['year'] = int(item['year'])
        return jsonify(item)


@app.route(f'{api_info_v2_prefix}/watch', methods=['POST'])
@auth.login_required
def add_watch():

    connection = get_connection()

    table = connection.Table('watches')

    try:
        response = table.put_item(Item=request.json)
    except ClientError as e:
        print(e.response['Error']['Message'])
        abort(404)
    else:
        return jsonify(success=True)

@app.after_request
def add_header(response):
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
