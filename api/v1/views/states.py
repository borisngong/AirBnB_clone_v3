#!/usr/bin/python3
"""Module for working with State objects and RESTFul API actions"""


from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


app = Flask(__name__)
"""Ensuring the necessary imports and Flask app initialization"""

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def obtain_all_states():
    """Responsible for retrieving the list of all State objects"""
    states = storage.all(State).values()
    json_response = [state.to_dict() for state in states]
    return jsonify(json_response)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def obtain_state_by_id(state_id):
    """Responsible for retrieving a specific State object by ID"""
    get_state = storage.get(State, state_id)
    if get_state is None:
        abort(404)
    return jsonify(get_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def remove_state(state_id):
    """Responsible for deleting a specific State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Responsible for creating a new State object."""
    state_json_data = request.get_json()
    if not state_json_data:
        abort(400, "Not a JSON")
    if 'name' not in state_json_data:
        abort(400, "Missing name")
    new_state = State(**state_json_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Responsible for Updating an existing State object."""
    up_state = storage.get(State, state_id)
    if up_state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(up_state, key, value)
    up_state.save()
    return jsonify(up_state.to_dict()), 200
