#!/usr/bin/python3
"""
view for City objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        "/states/<state_id>/cities",
        methods=['GET'],
        strict_slashes=False)
def retrive_cities_by_state(state_id):
    """ return list of all cities related to a state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route(
        "/cities/<city_id>",
        methods=['GET'],
        strict_slashes=False)
def retrive_city(city_id):
    """ used to retrive a specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        "/cities/<city_id>",
        methods=['DELETE'],
        strict_slashes=False)
def delete_city(city_id):
    """ used to delete an city object when"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/states/<state_id>/cities",
        methods=['POST'],
        strict_slashes=False)
def create_city(state_id):
    """ creates a new city object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if 'name' not in request_data:
        abort(400, description="Missing name")
    new_city = City()
    new_city.name = request_data['name']
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route(
        "/cities/<city_id>",
        methods=['PUT'],
        strict_slashes=False)
def update_city(city_id):
    """ updates an existing city object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at', 'state_id'):
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
