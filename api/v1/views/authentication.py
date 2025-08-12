#!/usr/bin/python3

from api.v1.views import auth_blueprint
from flask import abort, jsonify, make_response, request
from flask.views import MethodView
from models import storage, CNC
from models.user import User, BlacklistToken


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        all_users = storage.all('User').values()
        req_data = request.get_json()
        if req_data is None:
            abort(400, 'Not a JSON')
        email = req_data.get('email')
        if email is None:
            abort(400, 'Missing email')
        password = req_data.get('password')
        if password is None:
            abort(400, 'Missing password')
        for user in all_users:
            if user.email == email:
                abort(400, 'User already exists. Please Log in.')
        User = CNC.get('User')
        new_user = User(**req_data)
        new_user.save()
        auth_token = new_user.encode_auth_token(new_user.id)
        responseObject = {
            'status': 'success',
            'message': 'Successfully registered.',
            'user': new_user.to_json(),
            'auth_token': auth_token.decode()
        }
        return make_response(jsonify(responseObject)), 201


auth_blueprint.add_url_rule(
    '/register',
    view_func=RegisterAPI.as_view('register_api'),
    methods=['POST']
)


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        all_users = storage.all('User').values()
        req_data = request.get_json()
        email = req_data.get('email')
        password = req_data.get('password')
        user_obj = None
        for user in all_users:
            if user.email == email:
                user_obj = user
        if user_obj is None:
            abort(400, 'User not found. Please try another email or register.')
        secure_password = User.pass_encryption(password)
        if secure_password != user_obj.password:
            abort(400, 'Incorrect Password. Please try again or register.')
        auth_token = user_obj.encode_auth_token(user_obj.id)
        responseObject = {
            'status': 'success',
            'message': 'Successfully logged in.',
            'auth_token': auth_token.decode()
        }
        return make_response(jsonify(responseObject)), 200


auth_blueprint.add_url_rule(
    '/login',
    view_func=LoginAPI.as_view('login_api'),
    methods=['POST']
)


class UserAPI(MethodView):
    """
    User Resource
    """

    def get(self):
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
        all_users = storage.all('User').values()
        user_obj = None
        for user in all_users:
            if user.id == resp:
                user_obj = user
        if user_obj:
            responseObject = {
                'status': 'success',
                'data': user_obj.to_json()
            }
            return make_response(jsonify(responseObject)), 200
        abort(400, 'An error occurred.')


auth_blueprint.add_url_rule(
    '/status',
    view_func=UserAPI.as_view('user_api'),
    methods=['GET']
)


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
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
        try:
            blacklist_token = BlacklistToken(token=auth_token)
            blacklist_token.save()
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            abort(400, e)


auth_blueprint.add_url_rule(
    '/logout',
    view_func=LogoutAPI.as_view('logout_api'),
    methods=['POST']
)
