#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pymysql

db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_dbname = os.environ['DB_DBNAME']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']

http_user = os.environ['HTTP_USER']
http_pass = os.environ['HTTP_PASS']

api_info_v1_prefix = '/info/v1'

con = pymysql.connect(db_host, db_user, db_pass, db_dbname)

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == http_user:
        return check_password_hash(generate_password_hash(http_pass), password)
    return False


@app.route(f'{api_info_v1_prefix}/watch/<sku>', methods=['GET'])
@auth.login_required
def get_watch_data(sku):
    with con:
        cur = con.cursor(pymysql.cursors.DictCursor)

        cur.execute("select * from watches where sku=%s", sku)

        response = cur.fetchone()

        # If no watch found, return 404
        if response is None:
            abort(404)

    return jsonify(response)



@app.route(f'{api_info_v1_prefix}/watch', methods=['POST'])
@auth.login_required
def add_watch():
    with con:
        cur = con.cursor(pymysql.cursors.DictCursor)
        sql = f'insert into watches ({", ".join([k for k in request.json.keys()])}) values ({", ".join(["%s" for v in request.json.values()])})'
        try:
            cur.execute(sql, [v for v in request.json.values()])
        # Return 400 if e.g. an unexisting attribute has been specified, or if the sku already exists
        except pymysql.Error:
            abort(400)

    return jsonify(success=True)


@app.route(f'{api_info_v1_prefix}/watch/<sku>', methods=['DELETE'])
@auth.login_required
def delete_watch(sku):
    with con:
        cur = con.cursor(pymysql.cursors.DictCursor)
        try:
            cur.execute('delete from watches where sku = %s', sku)

            # If no rows has been affected by the delete, it means that the specified sku didn't exist, return 404
            if cur.rowcount == 0:
                abort(404)
        # If something other went wrong, return 400
        except pymysql.Error:
            abort(400)

    return jsonify(success=True)


@app.after_request
def add_header(response):
    # Headers to allow GET data to be valid 1 hour
    response.cache_control.max_age = 3600
    response.cache_control.public = True
    response.add_etag()

    # Headers for testing with swagger
    response.headers.add('Access-Control-Allow-Origin', 'https://editor.swagger.io')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, api_key, Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, DELETE, PUT, PATCH, OPTIONS')
    return response


if __name__ == '__main__':
    app.run(port=1080, debug=False, host='0.0.0.0')
