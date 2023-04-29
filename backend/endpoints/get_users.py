# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from backend import app, models, conf
from flask import jsonify, request, send_file, make_response
from backend.libs import http_methods
from io import StringIO, BytesIO
import csv


@app.route("/getUsers")
@http_methods.GET
def get_users():
    users_model = models.env["users"]
    response = {"status": "error"}  # default response
    if request.args.get("apiKey") == conf.app.API_KEY:
        users = users_model.search([])
        user_meal_data = []

        for user in users:
            meals = ""
            for meal in user.favorite_meal_ids:
                meals += "* " + meal.name + "\n"
            user_meal_data.append([user.uid, meals])

        # Creating a CSV file with the fetched data
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(["Name", "Favorite Meals"])

        for row in user_meal_data:
            csv_writer.writerow(row)

        # Reset the file pointer to the beginning
        csv_data.seek(0)
        csv_data_bytes = csv_data.getvalue().encode("utf-8")
        csv_data_io = BytesIO(csv_data_bytes)

        response = make_response(
            send_file(
                csv_data_io,
                mimetype="text/csv",
                as_attachment=True,
                download_name="users_favorite_meals.csv",
            )
        )

        # Set the Cache-Control header to prevent caching
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response
    else:
        return jsonify(response)
