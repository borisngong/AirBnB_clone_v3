#!/usr/bin/python3
"""This Module iss responsible for working with Amenities"""

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def obtain_all_amenities():
    """Responsible for retrieving the list of all Amenity objects"""
    b_amenities_data = storage.all(Amenity).values()
    b_amenities = [amenity.to_dict() for amenity in b_amenities_data]
    return jsonify(b_amenities), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def obtain_amenity(amenity_id):
    """Responsible for retrieving a specific Amenity object by ID"""
    b_amenity_data = storage.get(Amenity, amenity_id)
    if b_amenity_data is None:
        abort(404)
    return jsonify(b_amenity_data.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def remove_amenity(amenity_id):
    """Responsible for deleting a specific Amenity object by ID"""
    b_amenity_data = storage.get(Amenity, amenity_id)
    if b_amenity_data is None:
        abort(404)
    storage.delete(b_amenity_data)
    storage.save()
    json_response = jsonify({}), 200
    return json_response


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def make_new_amenity():
    """Responsible for creating a new Amenity"""
    amenity_json_data = request.get_json()
    if not amenity_json_data:
        abort(400, 'Not a JSON')
    if 'name' not in amenity_json_data:
        abort(400, 'Missing name')
    n_amenity = Amenity(**amenity_json_data)
    n_amenity.save()
    json_response = jsonify(n_amenity.to_dict()), 201
    return json_response


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def edit_update_amenity(amenity_id):
    """Responsible for updating a specific Amenity object by ID"""
    b_amenity_data = storage.get(Amenity, amenity_id)
    if b_amenity_data is None:
        abort(404)
    b_amenity_json_data = request.get_json()
    if b_amenity_json_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in b_amenity_json_data:
        abort(400, 'Missing name')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in b_amenity_json_data.items():
        if key not in ignore_keys:
            setattr(b_amenity_data, key, value)
    b_amenity_data.save()
    json_response = jsonify(b_amenity_data.to_dict()), 200
    return json_response
