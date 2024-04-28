#!/usr/bin/python3
"""Module responsible for the API endpoints"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def app_get_status():
    """Responsible to get the status of the API"""
    boro_api_status = {
        "status": "OK"
    }
    api_response = jsonify(boro_api_status), 200
    return api_response

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def retrieve_count_stats():
    """
    Responsible for retrieving the counts of all objects
    """
    b_object_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    json_response = jsonify(b_object_count)
    return json_response