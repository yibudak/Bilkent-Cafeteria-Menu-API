from flask import Flask
from backend.libs.config import Config
from flask_cors import CORS

__VERSION__ = "1.0.0"

app = Flask(__name__)
CORS(app)
conf = Config(path="/etc/bilkent_cafeteria_menu_api.conf")

# Initialize database and models
from backend import models

# Register endpoints
from backend.endpoints import endpoints

app.register_blueprint(endpoints)
