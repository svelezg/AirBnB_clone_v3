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


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
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
    states = []
    cities = []
    places = []
    places_result = []
    if not request.json:
        abort(400, 'Not a JSON')
    states_ids = request.json.get('states', "")
    if states_ids and len(states_ids) > 0:
        for the_id in request.json.get('states', ""):
            my_state = storage.get('State', the_id)
            if my_state is None:
                abort(404)
            states.append(my_state.to_dict())
            for my_city in my_state.cities:
                cities.append(my_city.to_dict())
                for my_place in my_city.places:
                    places.append(my_place)
    cities_ids = request.json.get('cities', "")
    if cities_ids and len(cities_ids) > 0:
        for the_id in request.json.get('cities', ""):
            my_city = storage.get('City', the_id)
            if my_city is None:
                abort(404)
            cities.append(my_city.to_dict())
            for my_place in my_city.places:
                places.append(my_place)
    if (not states_ids and not cities_ids) or (len(states_ids) == 0 and len(cities_ids) == 0):
        # print("No States and Cities")
        those_places = storage.all('Place').values()
        for my_places in those_places:
            places.append(my_places)
    amenities_ids = request.json.get('amenities', "")
    if amenities_ids and len(amenities_ids) > 0:
        # print("amenities is in")
        for my_place in places:
            the_place = storage.get('Place', my_place.id)
            """
            print("****{} {}***".format(my_place.id, my_place.name))
            for it in the_place.amenities:
                print("{} {}".format(it.id, storage.get('Amenity', it.id).name))
            """
            for the_id in request.json.get('amenities', ""):
                if the_id not in the_place.amenities:
                    # print("The place {} Does not have {} amenity".format(the_place.id, the_id))
                    places.remove(my_place)
                    break
    for my_place in places:
        places_result.append(my_place.to_dict())
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
