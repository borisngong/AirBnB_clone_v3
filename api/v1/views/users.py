#!/usr/bin/python3
"""This Module iss responsible for working with users"""


from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def obtain_all_users():
    """Responsible for retrieving the list of all User objects"""
    b_users_data = storage.all(User).values()
    users_data = [user.to_dict() for user in b_users_data]
    json_response = jsonify(users_data)
    return json_response


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def id_obtian_user(user_id):
    """Responsible for retrieving a specific User object by ID"""
    b_user_data = storage.get(User, user_id)
    if b_user_data is None:
        abort(404)
    json_response = jsonify(b_user_data.to_dict())
    return json_response


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def remove_user(user_id):
    """Responsible for deleting a specific User object by ID"""
    b_user_data = storage.get(User, user_id)
    if b_user_data is None:
        abort(404)
    storage.delete(b_user_data)
    storage.save()
    json_response = jsonify({}), 200
    return json_response


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def make_new_user():
    """Creates a new User"""
    user_json_data = request.get_json()
    if not user_json_data:
        abort(400, 'Not a JSON')
    if 'email' not in user_json_data:
        abort(400, 'Missing email')
    if 'password' not in user_json_data:
        abort(400, 'Missing password')
    n_user = User(**user_json_data)
    n_user.save()
    json_reponse = jsonify(n_user.to_dict()), 201
    return json_reponse


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def edit_update_user(user_id):
    """Responsible for updating a specific User object by ID"""
    b_user_data = storage.get(User, user_id)
    if b_user_data is None:
        abort(404)
    user_json_data = request.get_json()
    if user_json_data is None:
        abort(400, 'Not a JSON')
    disregard_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user_json_data.items():
        if key not in disregard_keys:
            setattr(b_user_data, key, value)
    b_user_data.save()
    json_response = jsonify(b_user_data.to_dict()), 200
    return json_response
