#!/usr/bin/python3
"""
Index page
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, user


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def users():
    """users"""
    users = []
    my_users = storage.all('User').values()
    for my_user in my_users:
        users.append(my_user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def user_id(user_id):
    """Retrieves a User object"""
    my_user = storage.get('User', user_id)
    if my_user is None:
        abort(404)
    return jsonify(my_user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_id_delete(user_id):
    """Deletes a User object"""
    my_user = storage.get('User', user_id)
    if my_user is None:
        abort(404)
    my_user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a User object"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    my_user = user.User(email=request.json.get('email', ""),
                        password=request.json.get('password', ""))
    storage.new(my_user)
    my_user.save()
    return make_response(jsonify(my_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    my_user = storage.get('User', user_id)
    if my_user is None:
        abort(404)
    if not request.json:
        # return make_response(jsonify({'error': 'Not a JSON'}), 400)
        abort(400, 'Not a JSON')
    for req in request.json:
        if req not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(my_user, req, request.json[req])
    my_user.save()
    return jsonify(my_user.to_dict())


if __name__ == "__main__":
    pass
