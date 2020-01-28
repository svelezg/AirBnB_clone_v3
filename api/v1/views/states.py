#!/usr/bin/python3
"""
Index page
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, state


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def states():
    """states"""
    states = []
    my_states = storage.all('State').values()
    for my_state in my_states:
        states.append(my_state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def state_id(state_id):
    """Retrieves a State object"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    return jsonify(my_state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_id_delete(state_id):
    """Deletes a State object"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    my_state.delete()
    my_state.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def create_state():
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    my_state = state.State(name=request.json.get('name', ""))
    storage.new(my_state)
    my_state.save()
    return make_response(jsonify(my_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    if not request.json:
        # return make_response(jsonify({'error': 'Not a JSON'}), 400)
        abort(400, 'Not a JSON')
    for req in request.json:
        if req in ['id', 'created_at', 'updated_at']:
            my_state.__dict__[req] = request.json[req]
    my_state.save()
    return jsonify(my_state.to_dict())


if __name__ == "__main__":
    pass
