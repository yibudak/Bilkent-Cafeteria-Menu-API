# # Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from . import db
from .base import BaseModel


class NutritionFacts(BaseModel, db.Model):
    __tablename__ = "nutrition_facts"

    energy = db.Column(db.String(50))
    fat = db.Column(db.String(50))
    carbohydrate = db.Column(db.String(50))
    protein = db.Column(db.String(50))
    menu_id = db.Column(db.Integer, db.ForeignKey("daily_menus.id"), nullable=False)

    def __repr__(self):
        return "<NutritionFact: %r>" % self.english_name

    def create_or_update(self, vals, commit=True):
        """
        Check if the nutrition fact is already in the database.
        :return:
        """
        menu = self.query.filter_by(menu_id=vals["menu_id"]).first()
        if not menu:
            menu = super().create(vals, commit)
        else:
            menu.energy = vals["energy"]
            menu.fat = vals["fat"]
            menu.carbohydrate = vals["carbohydrate"]
            menu.protein = vals["protein"]
            db.session.commit()
        return menu
