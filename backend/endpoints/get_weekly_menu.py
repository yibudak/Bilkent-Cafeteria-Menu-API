# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from backend import app, models, conf
from flask import jsonify, request
from backend.libs import http_methods


@app.route("/getWeeklyMenu")
@http_methods.GET
def get_weekly_menu():
    menu_model = models.env["daily_menus"]
    response = {"status": "error"}  # default response
    if request.args.get("apiKey") == conf.app.API_KEY:
        weekly_menu = menu_model.get_weekly_menu()
        if weekly_menu:
            data = {}
            for date, menus in weekly_menu.items():
                str_date = date.strftime("%d.%m.%Y")
                data[str_date] = {}
                for menu in menus:
                    data[str_date].update(
                        {
                            menu.menu_type: {
                                "id": menu.id,
                                "name": menu.name,
                                "english_name": menu.english_name,
                                "courses": [
                                    {
                                        "id": meal.id,
                                        "name": meal.name,
                                        "english_name": meal.english_name,
                                    }
                                    for meal in menu.meal_ids
                                ],
                            }
                        }
                    )
                    if menu.menu_type != "alternative":
                        """
                        Since alternative menus don't have nutrition facts,
                        we don't need to add them to the response.
                        """
                        nutrition_facts = menu.nutrition_facts[0]
                        data[str_date][menu.menu_type].update(
                            {
                                "nutrition_facts": {
                                    "energy": nutrition_facts.energy,
                                    "fat": nutrition_facts.fat,
                                    "carbohydrate": nutrition_facts.carbohydrate,
                                    "protein": nutrition_facts.protein,
                                },
                            }
                        )

            response = {"status": "success", "data": data}

    return jsonify(response)
