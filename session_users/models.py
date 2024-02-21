from .. import db

from typing import List

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class SessionUser(db.Model):
    __tablename__ = 'session_users'

    user_id = mapped_column(ForeignKey('users.id'), primary_key=True)
    session_id = mapped_column(ForeignKey('sessions.id'), primary_key=True)

    parking_location = mapped_column(Text, nullable=True)
    surfing_location = mapped_column(Text, nullable=True)

    session: Mapped['Session'] = relationship(back_populates='session_users')
    user: Mapped['User'] = relationship(back_populates='session_users')