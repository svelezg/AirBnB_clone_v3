#!/usr/bin/python3
"""
Index page
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, state, city


@app_views.route('/cities', methods=['GET'],
                 strict_slashes=False)
def cities():
    """cities"""
    cities = []
    my_cities = storage.all('City').values()
    for my_city in my_cities:
        cities.append(my_city.to_dict())
    return jsonify(cities)


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_state_id(state_id):
    """Retrieves a State object"""
    cities = []
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    for my_city in my_state.cities:
        cities.append(my_city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def city_id(city_id):
    """Retrieves a City object by id"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    return jsonify(my_city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_id_delete(city_id):
    """Deletes a City object by id"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    my_city.delete()
    storage.save()
    return jsonify({})


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json(silent=True):
        abort(400, 'Missing name')
    my_city = city.City(name=request.get_json('name', ""), state_id=state_id)
    storage.new(my_city)
    my_city.save()
    return make_response(jsonify(my_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    for key, value in request.get_json(silent=True).items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(my_city, key, value)
    my_city.save()
    return jsonify(my_city.to_dict())


if __name__ == "__main__":
    pass
