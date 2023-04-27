# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from . import db
from datetime import datetime


class PriorityColumn(db.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._creation_order = 1


class BaseModel(object):
    __table_args__ = {"extend_existing": True}

    id = PriorityColumn(db.Integer, primary_key=True)
    create_date = PriorityColumn(db.DateTime, nullable=False)

    @classmethod
    def browse(cls, id):
        if any(
            (isinstance(id, str) and id.isdigit(), isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def search(cls, domain):
        """
        Odoo ORM search method for SQLAlchemy
        """
        query = cls.query
        ops = {
            "in": lambda col, val: col.in_(val),
            "ilike": lambda col, val: col.ilike(val),
            "=": lambda col, val: col == val,
            "!=": lambda col, val: col != val,
            "<": lambda col, val: col < val,
            ">": lambda col, val: col > val,
            "<=": lambda col, val: col <= val,
            ">=": lambda col, val: col >= val,
            "like": lambda col, val: col.like(val),
            "not like": lambda col, val: ~col.like(val),
            "contains": lambda col, val: col.contains(val),
            "not contains": lambda col, val: ~col.contains(val),
            # add additional operators here as needed
        }
        stack = []
        for f in domain:
            if f == "|":
                right = stack.pop()
                left = stack.pop()
                query = query.filter(cls._combine_domain(left, right, "or"))
                stack.append(None)
            elif f == "&":
                stack.append(cls._create_filter(cls, f, ops))
            else:
                stack.append(cls._create_filter(cls, f, ops))
        if stack:
            group_filter = stack[0]
            for f in stack[1:]:
                group_filter &= f
            query = query.filter(group_filter)
        else:
            query = query.filter(None)
        return query.all()

    @staticmethod
    def _create_filter(model, f, ops):
        """
        Create a SQLAlchemy filter from an Odoo domain tuple
        """
        if f[1] in ops:
            col = model.__dict__[f[0]]
            return ops[f[1]](col, f[2])
        else:
            return None

    @staticmethod
    def _combine_domain(left, right, op):
        """
        Combine two SQLAlchemy filters with the given operator
        """
        if left is None:
            return right
        elif right is None:
            return left
        else:
            return left.op(op)(right)

    @classmethod
    def create(cls, vals, commit=True):
        if not vals.get("create_date", False):
            vals.update({"create_date": datetime.now()})
        instance = cls(**vals)
        db.session.add(instance)
        if commit:
            db.session.commit()
        return instance

    @classmethod
    def create_multi(cls, vals_list, commit=True):
        create_date = datetime.now()
        instances = [cls(**row, create_date=create_date) for row in vals_list]
        db.session.add_all(instances)
        if commit:
            db.session.commit()
        return instances

    @classmethod
    def write(cls, vals, commit=True):
        instance = cls
        for attr, value in vals.items():
            setattr(instance, attr, value)
        if commit:
            db.session.commit()
        return instance

    def unlink(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    # def write(self, commit=True, **kwargs):
    #     for attr, value in kwargs.iteritems():
    #         setattr(self, attr, value)
    #     return commit and self.save() or self
