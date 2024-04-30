#!/usr/bin/python3
"""This Module iss responsible for working with cities"""


from api.v1.views import app_views
from models.state import State
from models import storage
from flask import request, abort, jsonify
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def obtain_state_cities(state_id):
    """Responsible for retrieving all city objects of a specific state"""
    b_state_data = storage.get(State, state_id)
    if b_state_data is None:
        abort(404)
    b_cities_data = storage.all(City).values()
    b_state_cities = []
    for city in b_cities_data:
        if city.state_id == state_id:
            b_state_cities.append(city.to_dict())
    return jsonify(b_state_cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def obtain_city_by_state_id(city_id):
    """Responsible for returning a specific city object by ID"""
    b_city_data = storage.get(City, city_id)
    if b_city_data is None:
        abort(404)
    return jsonify(b_city_data.to_dict())


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def remove_sp_city(city_id):
    """Responsible for deleting a specific city object by ID"""
    b_city_data = storage.get(City, city_id)
    if b_city_data is None:
        abort(404)
    storage.delete(b_city_data)
    storage.save()
    json_response = jsonify({}), 200
    return json_response


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def sp_state_creation(state_id):
    """Responsible for creating a new object"""
    b_stae_data = storage.get(State, state_id)
    if b_stae_data is None:
        abort(404)
    b_json_data = request.get_json()
    if not b_json_data:
        abort(400, 'Not a JSON')
    if 'name' is None:
        abort(400, 'Missing name')
    b_json_data['state_id'] = state_id
    n_city = City(**b_json_data)
    n_city.save()
    return jsonify(n_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["POST"], strict_slashes=False)
def edit_update_city(city_id):
    """Responsible for updating """
    b_city_data = storage.get(City, city_id)
    if b_city_data is None:
        abort(400)
    b_jason_data = request.get_json()
    if b_jason_data is None:
        abort(400, 'Not a JSON')
    if 'name' is None:
        abort(400, 'Missing name')
    disregard_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in b_jason_data.items():
        if k not in disregard_keys:
            setattr(b_city_data, k, v)
    b_city_data.save()
    return jsonify(b_city_data.to_dict()), 200
