#!/usr/bin/python3
"""Module responsible for running the Flask application"""


from flask_cors import CORS
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify


app = Flask(__name__)


app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Responsible for closing the database connection after each request
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """
    Responsible for handling 404 error status and returns JSON response
    """
    json_error_message = {
        "error": "Not found"
    }

    error_json_response = jsonify(json_error_message), 400

    return error_json_response


if __name__ == '__main__':
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT)
