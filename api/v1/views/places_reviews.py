#!/usr/bin/python3
"""This Module iss responsible for working with places_reviews"""


from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def obtain_all_place_reviews(place_id):
    """Responsible retrieving the list of all Review objects of a Place"""
    b_place_data = storage.get(Place, place_id)
    if b_place_data is None:
        abort(404)
    reviews_data = b_place_data.reviews
    reviews = [review.to_dict() for review in reviews_data]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def id_obtain_review(review_id):
    """Responsible retrieving a specific Review object by ID"""
    b_review_data = storage.get(Review, review_id)
    if b_review_data is None:
        abort(404)
    json_response = jsonify(b_review_data.to_dict())
    return json_response


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def remove_review(review_id):
    """Responsible for deleting a specific Review object by ID"""
    b_review_data = storage.get(Review, review_id)
    if b_review_data is None:
        abort(404)
    storage.delete(b_review_data)
    storage.save()
    json_response = jsonify({}), 200
    return json_response


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def make_new_review(place_id):
    """Responsible for creating a new Review"""
    b_place_data = storage.get(Place, place_id)
    if b_place_data is None:
        abort(404)
    b_place_json_data = request.get_json()
    if not b_place_json_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in b_place_json_data:
        abort(400, 'Missing user_id')
    if 'text' not in b_place_json_data:
        abort(400, 'Missing text')
    user_id = b_place_json_data['user_id']
    user_data = storage.get(User, user_id)
    if user_data is None:
        abort(404)
    n_review = Review(place_id=place_id, user_id=user_id, **b_place_json_data)
    n_review.save()
    json_response = jsonify(n_review.to_dict()), 201
    return json_response


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def edit_update_review(review_id):
    """Updates a specific Review object by ID"""
    b_review_data = storage.get(Review, review_id)
    if b_review_data is None:
        abort(404)
    review_json_data = request.get_json()
    if review_json_data is None:
        abort(400, 'Not a JSON')
    disregard_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for k, v in review_json_data.items():
        if k not in disregard_keys:
            setattr(b_review_data, k, v)
    b_review_data.save()
    json_response = jsonify(b_review_data.to_dict()), 200
    return json_response
