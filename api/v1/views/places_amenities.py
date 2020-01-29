#!/usr/bin/python3
"""
Places Amenity view
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, place, amenity


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_place_id(place_id):
    """Retrieves a Place object"""
    amenities = []
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    for my_amenity in my_place.amenities:
        amenities.append(my_amenity.to_dict())
    return jsonify(amenities)


@app_views.route('places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def place_amenity_id_delete(place_id, amenity_id):
    """Deletes a Amenity object by id"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    if my_amenity not in my_place.amenities:
        abort(404)
    my_place.amenities.remove(my_amenity)
    my_place.save()
    return jsonify({})


@app_views.route('places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def add_amenity(place_id, amenity_id):
    """Creates a Amenity object"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    if my_amenity in my_place.amenities:
        return make_response(jsonify(my_amenity.to_dict()), 200)
    my_place.amenities.append(my_amenity)
    my_place.save()
    return make_response(jsonify(my_amenity.to_dict()), 201)


if __name__ == "__main__":
    pass
