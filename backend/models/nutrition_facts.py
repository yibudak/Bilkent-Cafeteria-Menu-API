# # Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from . import db
from .base import BaseModel


class Meals(BaseModel, db.Model):
    __tablename__ = "meals"

    name = db.Column(db.Text())
    english_name = db.Column(db.Text())

    def __repr__(self):
        return "<Meal: %r>" % self.english_name

    def create(self, vals, commit=True):
        """
        Check if the meal is already in the database.
        :return:
        """
        meal = self.query.filter_by(name=vals["name"]).first()
        if not meal:
            meal = super().create(vals, commit)
        return meal
