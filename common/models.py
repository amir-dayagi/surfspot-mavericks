from typing import List

from sqlalchemy import ForeignKey, Integer, Text, DateTime, Double
from sqlalchemy import Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.sql import func

from .. import db

group_user = db.Table(
    'group_users',
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = mapped_column(Integer, db.Sequence('users_id_seq'), nullable=False, primary_key=True)

    username = mapped_column(Text, unique=True, nullable=False)
    password = mapped_column(Text, nullable=False)

    groups: Mapped[List['Group']] = relationship(secondary=group_user, back_populates='users')
    location: Mapped['UserLocation'] = relationship(cascade='all, delete')

    def to_dict(self):
        return {
                'id': int(self.id),
                'username': str(self.username)
               }
    
    def to_dict_with_loc(self):
        return {
                'id': int(self.id),
                'username': str(self.username),
                'location': self.location.to_dict() if self.location else None
               }


class UserLocation(db.Model):
    __tablename__ = 'user_locations'

    id = mapped_column(Integer, db.Sequence('user_locations_id_seq'), nullable=False, primary_key=True)

    user_id = mapped_column(ForeignKey('users.id'), nullable=False)
    update_datetime = mapped_column(DateTime(True), nullable=False, server_default=func.now())
    latitude = mapped_column(Double, nullable=False)
    longitude = mapped_column(Double, nullable=False)

    def to_dict(self):
        return {
                'id': int(self.id),
                'update_datetime': self.update_datetime.replace(microsecond=0).isoformat(),
                'latitude': float(self.latitude),
                'longitude': float(self.longitude)
               }


class Spot(db.Model):
    __tablename__ = 'spots'

    id = mapped_column(Integer, db.Sequence('spots_id_seq'), nullable=False, primary_key=True)
    
    name = mapped_column(Text, nullable=True)
    latitude = mapped_column(Double, nullable = False)
    longitude = mapped_column(Double, nullable = False)
    radius = mapped_column(Double, nullable = False)

    def to_dict(self):
        return {"id": int(self.id),
                "name": str(self.name),
                "latitude": float(self.latitude),
                "longitude": float(self.longitude),
                "radius": float(self.radius)}