from typing import List

from sqlalchemy import Integer, Text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import db

class User(db.Model):
    __tablename__ = 'users'

    id = mapped_column(Integer, nullable=False, primary_key=True, server_default="nextval('users_id_seq'::regclass)")

    email = mapped_column(CITEXT, unique=True, nullable=False)
    password = mapped_column(Text, nullable=False)
    first_name = mapped_column(Text, nullable=False)
    last_name = mapped_column(Text, nullable=True)

    session_users: Mapped[List['SessionUser']] = relationship(back_populates='user')
