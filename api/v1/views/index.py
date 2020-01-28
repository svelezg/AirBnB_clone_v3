#!/usr/bin/python3
"""
Index page
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """stats"""
    my_amenity = storage.count("Amenity")
    my_cities = storage.count("City")
    my_places = storage.count("Place")
    my_reviews = storage.count("Review")
    my_states = storage.count("State")
    my_users = storage.count("User")
    return jsonify(amenities=my_amenity,
                   cities=my_cities,
                   places=my_places,
                   reviews=my_reviews,
                   states=my_states,
                   users=my_users)


if __name__ == "__main__":
    pass
