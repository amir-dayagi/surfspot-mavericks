from typing import List

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import db

class User(db.Model):
    __tablename__ = 'users'

    id = mapped_column(Integer, db.Sequence('users_id_seq'), nullable=False, primary_key=True)

    email = mapped_column(Text, unique=True, nullable=False)
    password = mapped_column(Text, nullable=False)
    first_name = mapped_column(Text, nullable=False)
    last_name = mapped_column(Text, nullable=True)

    session_users: Mapped[List['SessionUser']] = relationship(back_populates='user', cascade='all, delete-orphan')
