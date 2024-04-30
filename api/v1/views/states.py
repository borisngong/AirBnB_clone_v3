#!/usr/bin/python3
"""This Module iss responsible for working with states"""


from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def obtain_all_states():
    """Responsible for retrieving the list of all State objects"""
    states = storage.all(State).values()
    boro_json_reponse = [state.to_dict() for state in states]
    return jsonify(boro_json_reponse)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def obtain_state_by_id(state_id):
    """Responsible for retrieving a specific State object by ID"""
    state_data = storage.get(State, state_id)
    if state_data is None:
        abort(404)
    boro_json_response = state_data.to_dict()
    return jsonify(boro_json_response)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def remove_state_data(state_id):
    """Responsible for deleting a specific State object by ID"""
    state_data = storage.get(State, state_id)
    if state_data is None:
        abort(404)
    storage.delete(state_data)
    storage.save()
    json_response = jsonify({}), 200
    return json_response


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def make_state():
    """Responsible for creating a new State object"""
    state_json_data = request.get_json()
    if not state_json_data:
        abort(400, 'Not a JSON')
    if 'name' not in state_json_data:
        abort(400, 'Missing name')
    state = State(**state_json_data)
    state.save()
    boro_json_reponse = state.to_dict()
    json_response =jsonify(boro_json_reponse), 201
    return json_response


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def edit_update_state(state_id):
    """Update an existing State object"""
    state_json_data = storage.get(State, state_id)
    if state_json_data is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    disregard_keys = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in disregard_keys:
            setattr(state_json_data, k, v)
    state_json_data.save()
    boro_json_response = state_json_data.to_dict()
    json_response = jsonify(boro_json_response), 200
    return json_response
