#!/usr/bin/python3
"""Module responsible for the API endpoints"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def app_get_status(Exception):
    """Responsible to get the status of the API"""
    boro_api_status = {
        "status": "OK"
    }
    api_response = jsonify(boro_api_status), 200
    return api_response
