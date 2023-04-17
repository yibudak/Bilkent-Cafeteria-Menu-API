# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from backend import app, conf
from flask import jsonify, request
from backend.libs import http_methods, menu_scraper

"""
This is not a real endpoint for users. This endpoint is used
to call the method that parses the menu from the website.
So scheduling is done with crontab.
"""


@app.route("/parseMenu")
@http_methods.GET
def parse_menu():
    response = {"status": "error"}  # default response
    if request.args.get("apiKey") == conf.app.API_KEY:
        menu_scraper.scrap_menu()
        response = {"status": "success"}

    return jsonify(response)
