# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from backend import app, conf
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = conf.db.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from . import meals
from . import daily_menus
from . import nutrition_facts
from . import users

# Register models to app

env = {
    "meals": meals.Meals(),
    "daily_menus": daily_menus.DailyMenus(),
    "nutrition_facts": nutrition_facts.NutritionFacts(),
    "users": users.Users(),
}

# with app.app_context():
#     db.drop_all()
#     db.create_all()
