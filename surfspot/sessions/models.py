from .. import db

from typing import List

from sqlalchemy import inspect, DateTime, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import validates, Mapped, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

class Session(db.Model):
    __tablename__ = 'sessions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sessions_pkey'),
    )

    # auto generated fields
    id = mapped_column(Integer)
    create_datetime = mapped_column(DateTime(True)) # do this on database
    
    # input by user fields
    name = mapped_column(Text, nullable=False)
    start_datetime = mapped_column(DateTime(True))
    end_datetime = mapped_column(DateTime(True))
    area_location = mapped_column(Text)

    # TODO write validaters for values that can be null

    # session_users: Mapped[List['SessionUsers']] = relationship('SessionUsers', uselist=True, back_populates='session')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


    