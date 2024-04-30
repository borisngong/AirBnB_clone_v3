#!/usr/bin/python3
"""This Module iss responsible for working with places"""


from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def obtain_all_city_places(city_id):
    """Responsible for retrieving the list of all Place objects of a City"""
    city_data = storage.get(City, city_id)
    if city_data is None:
        abort(404)
    places_data = city_data.places
    places = [place.to_dict() for place in places_data]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def id_obtain_place(place_id):
    """Responsible retreving a specific Place object by ID"""
    place_data = storage.get(Place, place_id)
    if place_data is None:
        abort(404)
    json_response = jsonify(place_data.to_dict())
    return json_response


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def remove_place(place_id):
    """Responsible deleting a specific Place object by ID"""
    b_place_data = storage.get(Place, place_id)
    if b_place_data is None:
        abort(404)
    storage.delete(b_place_data)
    storage.save()
    json_response = jsonify({}), 200
    return json_response


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def make_new_place(city_id):
    """Responsible for creating a new Place"""
    b_city_data = storage.get(City, city_id)
    if b_city_data is None:
        abort(404)
    place_json_data = request.get_json()
    if not place_json_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in place_json_data:
        abort(400, 'Missing user_id')
    if 'name' not in place_json_data:
        abort(400, 'Missing name')
    user_id = place_json_data['user_id']
    user_data = storage.get(User, user_id)
    if user_data is None:
        abort(404)
    n_place = Place(city_id=city_id, user_id=user_id, **place_json_data)
    n_place.save()
    json_response = jsonify(n_place.to_dict()), 201
    return json_response


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def edit_update_place(place_id):
    """Responsible for working with a specific Place object by ID"""
    b_place_data = storage.get(Place, place_id)
    if b_place_data is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    disregard_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in disregard_keys:
            setattr(b_place_data, key, value)
    b_place_data.save()
    json_response = jsonify(b_place_data.to_dict()), 200
    return json_response
