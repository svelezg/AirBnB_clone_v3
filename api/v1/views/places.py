#!/usr/bin/python3
"""
Places view
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, city, place


@app_views.route('/places', methods=['GET'],
                 strict_slashes=False)
def places():
    """places"""
    places = []
    my_places = storage.all('Place').values()
    for my_place in my_places:
        places.append(my_place.to_dict())
    return jsonify(places)


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_city_id(city_id):
    """Retrieves a City object"""
    places = []
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    for my_place in my_city.places:
        places.append(my_place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def place_id(place_id):
    """Retrieves a Place object by id"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def place_id_delete(place_id):
    """Deletes a Place object by id"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    my_place.delete()
    storage.save()
    return jsonify({})


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    my_user = storage.get('User', request.json.get('user_id', ""))
    if my_user is None:
        abort(404)
    req = request.get_json(silent=True)
    req['city_id'] = city_id
    my_place = place.Place(**req)
    storage.new(my_place)
    my_place.save()
    return make_response(jsonify(my_place.to_dict()), 201)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_place():
    """places route to handle http method for request to search places"""
    if not request.is_json:
        abort(400, "Not a JSON")
    parameters = request.get_json()
    parameters_list = [len(parameter) for parameter in parameters.values()]
    if (len(parameters) is 0) or (max(parameters_list) is 0):
        places = storage.all("Place").values()
        return jsonify([item.to_dict() for item in places])

    places_result = []
    places = []
    places_obj = []

    if 'states' in parameters and len(parameters.get('states')) > 0:
        states_ids = parameters.get('states')
        states = [storage.get('State', state) for state in states_ids]
        for my_state in states:
            for my_city in my_state.cities:
                for my_place in my_city.places:
                    places.append(my_place.to_dict())
                    places_obj.append(my_place)

    if 'cities' in parameters and len(parameters.get('cities')) > 0:
        cities_ids = parameters.get('cities')
        cities = [storage.get('City', city) for city in cities_ids]
        for city in cities:
            city_places = city.places
            for my_place in city_places:
                places.append(my_place.to_dict())
                places_obj.append(my_place)

    if 'amenities' in parameters and len(parameters.get('amenities')) > 0:
        amenities_ids = parameters.get('amenities')
        if len(places_obj) == 0:
            places_obj = storage.all('Place').values()
        else:
            places = []

        flag = True
        for my_place in places_obj:
            available_amenity = []
            amenities_auxiliary = my_place.amenities
            for amenity_auxiliary in amenities_auxiliary:
                available_amenity.append(amenity_auxiliary.id)
            for amenity in amenities_ids:
                if amenity in available_amenity:
                    flag = True
                else:
                    flag = False
                    break
            if flag:
                aux_place = my_place.to_dict()
                del aux_place['amenities']
                places.append(aux_place)
    n = 0
    for my_place in places:
        n = n + 1
        if my_place not in places[n:]:
            places_result.append(my_place)
    # print("Without repeats {}".format(len(places_result)))
    return jsonify(places_result)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    if not request.json:
        # return make_response(jsonify({'error': 'Not a JSON'}), 400)
        abort(400, 'Not a JSON')
    for req in request.get_json(silent=True):
        if req not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(my_place, req, request.json[req])
    my_place.save()
    return jsonify(my_place.to_dict())


if __name__ == "__main__":
    pass
