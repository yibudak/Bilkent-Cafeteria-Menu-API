# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from flask import Blueprint
from .get_weekly_menu import get_weekly_menu
from .parse_menu import parse_menu

endpoints = Blueprint(
    "endpoints",
    __name__,
)
