#!/usr/bin/python3
""" This model handels the view routes
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from flask import jsonify
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """ returns the status of my API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def number_of_objects():
    """ return the number of each object by type"""
    output = {}
    objects = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State, "users": User}
    for key, obj in objects.items():
        output[key] = storage.count(obj)

    return jsonify(output)
