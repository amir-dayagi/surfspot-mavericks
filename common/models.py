from typing import List

from sqlalchemy import ForeignKey, Integer, Text
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

    def to_dict(self):
        return {"id": int(self.id),
                "email": str(self.email),
                "first_name": str(self.first_name),
                "last_name": str(self.last_name)}



class SessionUser(db.Model):
    __tablename__ = 'session_users'

    user_id = mapped_column(ForeignKey('users.id'), primary_key=True)
    session_id = mapped_column(ForeignKey('sessions.id'), primary_key=True)

    parking_location = mapped_column(Text, nullable=True)

    session: Mapped['Session'] = relationship(back_populates='session_users')
    user: Mapped['User'] = relationship(back_populates='session_users')