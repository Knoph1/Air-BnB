#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC, User
from flasgger.utils import swag_from


@app_views.route('/users/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/users_no_id.yml', methods=['GET', 'POST'])
def users_no_id(user_id=None):
    """
        users route that handles http requests with no ID given
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            abort(400, 'Bearer token malformed.')
    else:
        abort(400, 'Provide a valid auth token.')
    resp = User.decode_auth_token(auth_token)
    if 'Please log in again.' in resp:
        abort(400, resp)

    if request.method == 'GET':
        all_users = storage.all('User')
        all_users = [obj.to_json() for obj in all_users.values()]
        return jsonify(all_users)

    if request.method == 'POST':
        req_data = request.get_json()
        if req_data is None:
            abort(400, 'Not a JSON')
        if req_data.get('email') is None:
            abort(400, 'Missing email')
        if req_data.get('password') is None:
            abort(400, 'Missing password')
        User = CNC.get('User')
        new_object = User(**req_data)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/users_id.yml', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id=None):
    """
        users route that handles http requests with ID given
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            abort(400, 'Bearer token malformed.')
    else:
        abort(400, 'Provide a valid auth token.')
    resp = User.decode_auth_token(auth_token)
    if 'Please log in again.' in resp:
        abort(400, resp)

    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(user_obj.to_json())

    if request.method == 'DELETE':
        user_obj.delete()
        del user_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_data = request.get_json()
        if req_data is None:
            abort(400, 'Not a JSON')
        user_obj.bm_update(req_data)
        return jsonify(user_obj.to_json()), 200
