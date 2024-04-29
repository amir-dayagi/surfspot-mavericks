from sqlalchemy import Double, Integer, Text
from sqlalchemy.orm import mapped_column

from .. import db

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