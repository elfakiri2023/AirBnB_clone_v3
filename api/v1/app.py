#!/usr/bin/python3
""" This is the main flask app"""
from api.v1.views import app_views
from flask_cors import CORS
from os import environ
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)
""" This is the main flask app"""
app.register_blueprint(app_views)
CORS(app, origins='0.0.0.0')


@app.teardown_appcontext
def teardown_db(exception=None):
    """ called each time the database is updated"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handle status_code 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = environ.get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
