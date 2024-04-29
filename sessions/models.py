from typing import List

from sqlalchemy import DateTime, Double, inspect, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .. import db

class Session(db.Model):
    __tablename__ = 'sessions'

    id = mapped_column(Integer, db.Sequence('sessions_id_seq'), nullable=False, primary_key=True)
    create_datetime = mapped_column(DateTime(True), nullable=False, server_default=func.now())

    name = mapped_column(Text, nullable=False)
    start_datetime = mapped_column(DateTime(True), nullable=False)
    spot_id = mapped_column(ForeignKey('spots.id'), nullable=False)

    spot: Mapped['Spot'] = relationship()
    session_users: Mapped[List['SessionUser']] = relationship(back_populates='session', cascade='all, delete-orphan')


    def to_dict(self):
        return {"id": int(self.id),
                "create_datetime": self.create_datetime.replace(microsecond=0).isoformat(),
                "name": str(self.name),
                "start_datetime": self.start_datetime.replace(microsecond=0).isoformat(),
                "spot": self.spot.to_dict()}
