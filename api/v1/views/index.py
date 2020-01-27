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


if __name__ == "__main__":
    pass
