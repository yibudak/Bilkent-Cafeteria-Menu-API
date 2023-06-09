# # Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from . import db
from .base import BaseModel
from datetime import datetime, timedelta

meal_menu_rel = db.Table(
    "meal_menu_rel",
    db.Column("meal_id", db.Integer, db.ForeignKey("meals.id")),
    db.Column("menu_id", db.Integer, db.ForeignKey("daily_menus.id")),
    db.Column("sequence", db.Integer),
)


class DailyMenus(BaseModel, db.Model):
    __tablename__ = "daily_menus"

    date = db.Column(db.Date())
    name = db.Column(db.String(50))
    english_name = db.Column(db.String(50))
    nutrition_facts = db.relationship('NutritionFacts', backref='nutrition_facts', lazy=True)
    menu_type = db.Column(db.Text())
    meal_ids = db.relationship(
        "Meals",
        secondary=meal_menu_rel,
        lazy="subquery",
        backref=db.backref("menu_ids", lazy=True),
        order_by=meal_menu_rel.c.sequence,
    )

    def __repr__(self):
        return "<Menu %s (%s)>" % (self.date, self.menu_type)

    def create_or_update(self, vals, commit=True):
        """
        Check if the menu is already in the database.
        :return:
        """
        menu = self.query.filter_by(
            date=vals["date"], menu_type=vals["menu_type"]
        ).first()
        if not menu:
            menu = super().create(vals, commit)
        else:
            menu.meal_ids = vals["meal_ids"]
            db.session.commit()
        return menu

    def get_weekly_menu(self):
        """
        Get the weekly menu of the current day.
        :return:
        """
        today = datetime.today()
        start_of_current_week = (today - timedelta(days=today.weekday())).date()
        end_of_current_week = start_of_current_week + timedelta(days=6)
        menu = (
            self.query.filter(
                DailyMenus.date >= start_of_current_week,
                DailyMenus.date <= end_of_current_week,
            )
            .order_by(DailyMenus.date)
            .all()
        )

        grouped_menus = {}
        for item in menu:
            if item.date not in grouped_menus:
                grouped_menus[item.date] = [item]
            else:
                grouped_menus[item.date].append(item)

        return grouped_menus
