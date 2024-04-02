#!/usr/bin/python3
"""
view for Place objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def retrive_places_by_city(city_id):
    """ return list of places users """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route(
        "/places/<place_id>",
        methods=['GET'],
        strict_slashes=False)
def retrive_place(place_id):
    """ is used to retrive a specific place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        "/places/<place_id>",
        methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id):
    """ used to delete a place object when"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Not a JSON")

    if 'user_id' not in request_data:
        abort(400, "Missing user_id")

    user = storage.get(User, request_data["user_id"])
    if user is None:
        abort(404)

    if 'name' not in request_data:
        abort(400, "Missing name")

    new_place = Place(city_id=city_id, **request_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ updates an existing place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Not a JSON")

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
