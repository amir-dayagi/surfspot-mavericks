from .. import db

from typing import List

from sqlalchemy import DateTime, inspect, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Session(db.Model):
    __tablename__ = 'sessions'

    id = mapped_column(Integer, nullable=False, primary_key=True, server_default="nextval('sessions_id_seq'::regclass)")
    create_datetime = mapped_column(DateTime(True), nullable=False, server_default="now()")

    name = mapped_column(Text, nullable=False)
    start_datetime = mapped_column(DateTime(True), nullable=False)
    area = mapped_column(Text, nullable=False)

    session_users: Mapped[List['SessionUser']] = relationship(back_populates='session')


    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    