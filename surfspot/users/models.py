from .. import db

from typing import List

from sqlalchemy import inspect, Integer, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import validates, Mapped, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_unique_email')
    )

    # auto generated fields
    id = mapped_column(Integer)

    # input by user fields
    name = mapped_column(Text, nullable=False)
    email = mapped_column(Text)

    # session_users: Mapped[List['SessionUsers']] = relationship('SessionUsers', uselist=True, back_populates='user')

    @validates('email')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and not value:
            return None
        return value


    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
