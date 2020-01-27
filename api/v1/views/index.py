#!/usr/bin/python3
"""
Index page
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage

my_stats = {
  "amenities": 0,
  "cities": 0,
  "places": 0,
  "reviews": 0,
  "states": 0,
  "users": 0
}


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """stats"""
    my_stats['amenities'] = storage.count("Amenity")
    my_stats['cities'] = storage.count("City")
    my_stats['places'] = storage.count("Place")
    my_stats['reviews'] = storage.count("Review")
    my_stats['states'] = storage.count("State")
    my_stats['users'] = storage.count("User")
    return jsonify(my_stats)


if __name__ == "__main__":
    pass
