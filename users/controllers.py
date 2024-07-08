from datetime import datetime

from .. import db
from ..common.models import User, UserLocation


def get_users(search_query, limit):
    return db.session.scalars(db.select(User).where(User.username.contains(search_query))).all()[:limit]

def update_location(user, update_location_request):
    if not all(key in update_location_request for key in ('latitude', 'longitude')):
        raise JsonException('Missing required fields!', 401)
    
    user_location = db.session.scalar(db.select(UserLocation).where(UserLocation.user_id == user.id))
    try:
        if user_location:
            user_location.latitude = float(update_location_request['latitude'])
            user_location.longitude = float(update_location_request['longitude'])
            user_location.update_datetime = datetime.now()
        else:
            new_user_location = UserLocation(
                user_id = user.id,
                latitude = float(update_location_request['latitude']),
                longitude = float(update_location_request['longitude'])
            )
            db.session.add(new_user_location)
        db.session.commit()
    except ValueError:
        raise JsonException('Latitude and Longitude must be valid float types!', 401)