# # Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from . import db
from .base import BaseModel

user_meal_rel = db.Table(
    "user_meal_rel",
    db.Column("meal_id", db.Integer, db.ForeignKey("meals.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
)


class Users(BaseModel, db.Model):
    __tablename__ = "users"

    uid = db.Column(db.String(16))
    favorite_meal_ids = db.relationship(
        "Meals",
        secondary=user_meal_rel,
        lazy="subquery",
        backref=db.backref("user_ids", lazy=True),
    )

    def __repr__(self):
        return "<User: %r>" % self.uid

    def create(self, vals, commit=True):
        """
        Check if the user is already in the database.
        :return:
        """
        user = self.query.filter_by(uid=vals["uid"]).first()
        if not user:
            user = super().create(vals, commit)
        return user
