#!/usr/bin/python3


from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", methods=['GET'])
def app_get_status():
    boro_api_status = {
        "status": "OK"
    }
    api_responds = jsonify(boro_api_status), 200

    return api_responds


