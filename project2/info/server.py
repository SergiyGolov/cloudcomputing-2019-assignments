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

app = Flask(__name__)
auth = HTTPBasicAuth()

def create_connection():
    return pymysql.connect(db_host, db_user, db_pass, db_dbname)

@auth.verify_password
def verify_password(username, password):
    if username == http_user:
        return check_password_hash(generate_password_hash(http_pass), password)
    return False

@app.route(f'{api_info_v1_prefix}/', methods=['GET'])
def home():
    return jsonify("Health check hello.")


@app.route(f'{api_info_v1_prefix}/watch/<sku>', methods=['GET'])
@auth.login_required
def get_watch_data(sku):
    con = create_connection()
    try:
        with con:
            cur = con.cursor(pymysql.cursors.DictCursor)

            cur.execute("select * from watches where sku=%s", sku)

            response = cur.fetchone()

            # If no watch found, return 404
            if response is None:
                abort(404)
    
        return jsonify(response)

    finally:
        con.close()

@app.route(f'{api_info_v1_prefix}/watch/find')
@auth.login_required
def find_watch():
    con = create_connection()
    find_params = {}

    find_params['sku'] = request.args.get('sku', None)
    find_params['type'] = request.args.get('type', None)
    find_params['status'] = request.args.get('status', None)
    find_params['gender'] = request.args.get('gender', None)
    find_params['year'] = request.args.get('year', None)

    # allow finding by partial sku
    if find_params['sku'] is not None:
        find_params['sku'] += '%'

    try:
        with con:
            cur = con.cursor(pymysql.cursors.DictCursor)

            sql = "select * from watches"

            first_where = True

            for k, v in find_params.items():
                if k == 'sku':
                    equals = 'like'
                else:
                    equals = '='
                if v is not None and first_where:
                    sql += f" where {k} {equals} %s"
                    first_where = False
                elif v is not None and not first_where:
                    sql += f" and {k} {equals} %s"

            cur.execute(sql, [v for v in find_params.values() if v is not None])

            response = cur.fetchall()

            # If no watches found, return 404
            if len(response) == 0:
                abort(404)

        return jsonify(response)

    finally:
        con.close()


@app.route(f'{api_info_v1_prefix}/watch/complete-sku/<prefix>')
@auth.login_required
def complete_sku(prefix):
    con = create_connection()
    prefix += '%'  # add wildcard for sql query
    try:
        with con:
            cur = con.cursor(pymysql.cursors.DictCursor)

            cur.execute('select sku from watches where sku like %s', prefix)

            response = cur.fetchall()

            # If no sku corresponds to the prefix, return 404
            if len(response) == 0:
                abort(404)

        return jsonify(response)

    finally:
        con.close()


@app.route(f'{api_info_v1_prefix}/watch', methods=['POST'])
@auth.login_required
def add_watch():
    con = create_connection()
    try:
        with con:
            cur = con.cursor(pymysql.cursors.DictCursor)
            sql = f'insert into watches ({", ".join([k for k in request.json.keys()])}) values ({", ".join(["%s" for v in request.json.values()])})'
            try:
                cur.execute(sql, [v for v in request.json.values()])
            # Return 400 if e.g. an unexisting attribute has been specified, or if the sku already exists
            except pymysql.Error:
                abort(400)

        return jsonify(success=True)

    finally:
        con.close()


@app.route(f'{api_info_v1_prefix}/watch/<sku>', methods=['DELETE'])
@auth.login_required
def delete_watch(sku):
    con = create_connection()
    try:
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

    finally:
        con.close()


@app.route(f'{api_info_v1_prefix}/watch/<sku>', methods=['PUT'])
@auth.login_required
def update_watch(sku):
    con = create_connection()
    update_params = {}

    update_params['sku'] = request.get_json().get('sku', None)
    update_params['type'] = request.get_json().get('type', None)
    update_params['status'] = request.get_json().get('status', None)
    update_params['gender'] = request.get_json().get('gender', None)
    update_params['year'] = request.get_json().get('year', None)
    update_params['dial_material'] = request.get_json().get('dial_material', None)
    update_params['dial_color'] = request.get_json().get('dial_color', None)
    update_params['case_material'] = request.get_json().get('case_material', None)
    update_params['case_form'] = request.get_json().get('case_form', None)
    update_params['bracelet_material'] = request.get_json().get('bracelet_material', None)
    update_params['movement'] = request.get_json().get('movement', None)

    try:

        # Workaround: otherwise, it will return a 404 error if the new sku is equal to the old sku (a 400 error is more clear than a 404 error in this case)
        if update_params['sku'] is not None and update_params['sku'] == sku:
            abort(400)

        with con:
            cur = con.cursor(pymysql.cursors.DictCursor)

            sql = 'update watches set ' + ', '.join([f'{k} = %s' for k, v in update_params.items() if v is not None]) + ' where sku = %s'
            try:
                cur.execute(sql, [v for v in update_params.values() if v is not None]+[sku])

                # If no rows has been updated, it means that the specified sku doesn't exist, return 404
                if cur.rowcount == 0:
                    abort(404)

            # If invalid input, return 400
            except pymysql.Error:
                abort(400)

        return jsonify(success=True)
        
    finally:
        con.close()


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
