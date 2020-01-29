#!/usr/bin/python3
"""
Index page
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    """amenities"""
    amenities = []
    my_amenities = storage.all('Amenity').values()
    for my_amenity in my_amenities:
        amenities.append(my_amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """Retrieves a Amenity object"""
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    return jsonify(my_amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_id_delete(amenity_id):
    """Deletes a Amenity object"""
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    my_amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a Amenity object"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    my_amenity = amenity.Amenity(name=request.json.get('name', ""))
    storage.new(my_amenity)
    my_amenity.save()
    return make_response(jsonify(my_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    if not request.json:
        # return make_response(jsonify({'error': 'Not a JSON'}), 400)
        abort(400, 'Not a JSON')
    for req in request.json:
        if req not in ['id', 'created_at', 'updated_at']:
            setattr(my_amenity, req, request.json[req])
    my_amenity.save()
    return jsonify(my_amenity.to_dict())


if __name__ == "__main__":
    pass
