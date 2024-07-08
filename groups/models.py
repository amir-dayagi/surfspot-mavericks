from typing import List

from sqlalchemy import ForeignKey, Integer, Text, DateTime, ForeignKeyConstraint
from sqlalchemy import Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .. import db
from ..common.models import group_user

class Group(db.Model):
    __tablename__ = 'groups'

    id = mapped_column(Integer, db.Sequence('groups_id_seq'), nullable=False, primary_key=True)

    name = mapped_column(Text, nullable=False)
    session_id = mapped_column(ForeignKey('sessions.id'), nullable=True)
    
    users: Mapped[List['User']] = relationship(secondary=group_user, back_populates='groups')
    session: Mapped['Session'] = relationship()

    def to_dict(self):
        d = {
             'id': int(self.id),
             'name': str(self.name),
             'session': None
            }
        if self.session:
            d['session'] = self.session.to_dict()
        return d

class Session(db.Model):
    __tablename__ = 'sessions'

    id = mapped_column(Integer, db.Sequence('sessions_id_seq'), nullable=False, primary_key=True)

    start_datetime = mapped_column(DateTime(True), nullable=False)
    spot_id = mapped_column(ForeignKey('spots.id'), nullable=False)

    spot: Mapped['Spot'] = relationship()

    def to_dict(self):
        return {
                'id': int(self.id),
                'start_datetime': self.start_datetime.replace(microsecond=0).isoformat(),
                'spot': self.spot.to_dict()
               }

session_user = db.Table(
    'session_users',
    Column('user_id', primary_key=True),
    Column('group_id', primary_key=True),
    Column('session_id', ForeignKey('sessions.id', ondelete='CASCADE'), primary_key=True),
    ForeignKeyConstraint(['user_id', 'group_id'],
                         ['group_users.user_id', 'group_users.group_id'],
                         ondelete='CASCADE')
)

class Message(db.Model):
    __tablename__ = 'messages'

    id = mapped_column(Integer, db.Sequence('messages_id_seq'), nullable=False, primary_key=True)

    user_id = mapped_column(ForeignKey('users.id'))
    group_id = mapped_column(ForeignKey('groups.id'))
    context = mapped_column(Text, nullable=False)
    send_datetime = mapped_column(DateTime(True), nullable=False, server_default=func.now())

    def to_dict(self):
        return {
                'id': int(self.id),
                'user_id': int(self.user_id),
                'group_id': int(self.group_id),
                'context': str(self.context),
                'send_datetime': self.send_datetime.replace(microsecond=0).isoformat()
               }