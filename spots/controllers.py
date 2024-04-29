from .. import db
from .models import Spot
from ..common.utils import JsonException


def get_spots():
    return db.session.scalars(db.select(Spot)).all()

def get_spot(spot_id):
    spot = db.session.scalar(db.select(Spot).where(Spot.id == spot_id))

    if not spot:
        raise JsonException('Spot not found!', 404)
    
    return spot

def create_spot(spot_json):
    if not all(key in spot_json for key in ('name', 'latitude', 'longitude', 'radius')):
        raise JsonException('Missing required fields!', 400)

    new_spot = Spot(
                    name = spot_json['name'],
                    latitude = spot_json['latitude'],
                    longitude = spot_json['longitude'],
                    radius = spot_json['radius']
                    )
    
    db.session.add(new_spot)
    db.session.commit()
    db.session.refresh(new_spot)
    return new_spot
    

def delete_session(spot_id):
    spot = get_spot(spot_id)
    db.session.delete(spot)
    db.session.commit()