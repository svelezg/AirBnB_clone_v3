#!/usr/bin/python3
"""
Places Review view
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, place, review


@app_views.route('/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews():
    """reviews"""
    reviews = []
    my_reviews = storage.all('Review').values()
    for my_review in my_reviews:
        reviews.append(my_review.to_dict())
    return jsonify(reviews)


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_place_id(place_id):
    """Retrieves a Place object"""
    reviews = []
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    for my_review in my_place.reviews:
        reviews.append(my_review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def review_id(review_id):
    """Retrieves a Review object by id"""
    my_review = storage.get('Review', review_id)
    if my_review is None:
        abort(404)
    return jsonify(my_review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_id_delete(review_id):
    """Deletes a Review object by id"""
    my_review = storage.get('Review', review_id)
    if my_review is None:
        abort(404)
    my_review.delete()
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'text' not in request.json:
        abort(400, 'Missing text')
    my_user = storage.get('User', request.json.get('user_id', ""))
    if my_user is None:
        abort(404)
    req = request.get_json(silent=True)
    req['place_id'] = place_id
    my_review = review.Review(**req)
    storage.new(my_review)
    my_review.save()
    return make_response(jsonify(my_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    my_review = storage.get('Review', review_id)
    if my_review is None:
        abort(404)
    if not request.json:
        # return make_response(jsonify({'error': 'Not a JSON'}), 400)
        abort(400, 'Not a JSON')
    for req in request.get_json(silent=True):
        if req not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(my_review, req, request.json[req])
    my_review.save()
    return jsonify(my_review.to_dict())


if __name__ == "__main__":
    pass
