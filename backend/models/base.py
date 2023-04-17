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
    def search(cls, id):
        if any(
            (isinstance(id, str) and id.isdigit(), isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None

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

    def unlink(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    # def write(self, commit=True, **kwargs):
    #     for attr, value in kwargs.iteritems():
    #         setattr(self, attr, value)
    #     return commit and self.save() or self
