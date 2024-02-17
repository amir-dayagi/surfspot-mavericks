from .. import db

from typing import List

from sqlalchemy import inspect, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import validates, Mapped, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

class SessionUser(db.Model):
    __tablename__ = 'session_users'
    __table_args__ = (
        ForeignKeyConstraint(['session_id'], ['sessions.id'], name='session_users_session_fk'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='session_users_user_fk'),
        PrimaryKeyConstraint('user_id', 'session_id', name='session_users_pkey')
    )

    user_id = mapped_column(Integer, nullable=False)
    session_id = mapped_column(Integer, nullable=False)
    parking_location = mapped_column(Text)
    surf_location = mapped_column(Text)

    session: Mapped['Sessions'] = relationship('Sessions', back_populates='session_users')
    user: Mapped['Users'] = relationship('Users', back_populates='session_users')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    

    