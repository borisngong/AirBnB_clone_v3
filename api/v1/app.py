#!/usr/bin/python3


from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


# Register_blueprint app_view to Flask instance app
app.register_blueprint(app_views)


# Method to handle app teardown
@app.teardown_appcontext
def teardown_appcontext(self):
    """Respondible for closing database connection after each request"""
    storage.close()


if __name__ == '__main__':
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)