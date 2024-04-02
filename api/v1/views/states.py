#!/usr/bin/python3
"""
view for State objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_all_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route(
        "/states/<state_id>",
        methods=['GET'],
        strict_slashes=False)
def retrive_state(state_id):
    """ is used to retrive a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        "/states/<state_id>",
        methods=['DELETE'],
        strict_slashes=False)
def delete_state(state_id):
    """ is used to delete an state object when"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/states",
        methods=['POST'],
        strict_slashes=False)
def create_state():
    """ creates a new state"""
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    request_data = request.get_json()

    if 'name' not in request_data:
        abort(400, "Missing name")
    new_state = State()
    new_state.name = request_data.get('name')
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route(
        "/states/<state_id>",
        methods=['PUT'],
        strict_slashes=False)
def update_state(state_id):
    """ updates an existing state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
