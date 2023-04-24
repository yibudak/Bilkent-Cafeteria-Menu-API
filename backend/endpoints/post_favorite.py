# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from backend import app, conf, models
from flask import jsonify, request
from backend.libs import http_methods
from flask_expects_json import expects_json


API_SCHEMA = {
    "type": "object",
    "properties": {
        "apiKey": {"type": "string"},
        "userId": {"type": "string"},
        "favoriteMeals": {"type": "array"},
    },
    "required": ["apiKey", "userId", "favoriteMeals"],
}


@app.route("/postFavorite")
@expects_json(API_SCHEMA, silent=True)
@http_methods.POST
def post_favorite():
    response = {"status": "error"}  # default response
    users_model = models.env["users"]
    meals_model = models.env["meals"]
    if request.json["apiKey"] == conf.app.API_KEY:
        meals = meals_model.search([("id", "in", request.json["favoriteMeals"])])
        user = users_model.create({"uid": request.json["userId"]})
        user.favorite_meals = meals
        response = {"status": "success"}

    return jsonify(response)
