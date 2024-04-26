#!/usr/bin/python3


from api.v1.views import app_views
from flask import Response, json

@app_views.route("/status", methods=['GET'])
def app_get_status():
    response = {
        "status": "OK"
    }
    json_response = json.dumps(response, indent=4, separators=(',', ': '))
    json_response_with_newline = json_response + '\n'
    return Response(json_response_with_newline, content_type='application/json')