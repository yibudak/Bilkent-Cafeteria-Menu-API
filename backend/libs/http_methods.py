# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from functools import wraps

"""
Since we don't use classic way to generate endpoints,
we need to add methods with decorators. This module contains
decorators to add methods to the dispatchers

Note 6 March, 2023: We don't need to decorate the dispatchers
but it looks cool.
"""


def GET(func):
    """Adds GET method to the endpoint."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    if not hasattr(wrapper, "methods"):
        wrapper.methods = ["GET"]
    else:
        wrapper.methods = wrapper.methods + ["GET"]
    return wrapper


def POST(func):
    """Adds POST method to the endpoint."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    if not hasattr(wrapper, "methods"):
        wrapper.methods = ["POST"]
    else:
        wrapper.methods = wrapper.methods + ["POST"]

    return wrapper
