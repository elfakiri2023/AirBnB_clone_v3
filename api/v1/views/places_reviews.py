#!/usr/bin/python3
"""
view for Review object that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
        "/places/<place_id>/reviews",
        methods=['GET'],
        strict_slashes=False)
def retrive_reviews_of_place(place_id):
    """ return list of all reviews for place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def retrive_review(review_id):
    """ is used to retrive a specific review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ is used to delete an review object when"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ creates a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in data:
        abort(400, "Missing text")

    n_review = Review(place_id=place_id, **data)
    n_review.save()
    return jsonify(n_review.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        methods=['PUT'],
        strict_slashes=False)
def update_review(review_id):
    """ updates an existing review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at',
                       'city_id', 'place_id'):
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
