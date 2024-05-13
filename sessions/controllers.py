from datetime import datetime

from .. import db
from .models import Session
from ..common.models import User
from ..common.models import SessionUser
from ..common.utils import JsonException


def get_sessions(user):
    return [session_user.session for session_user in user.session_users]

def get_session(user, session_id):
    for session_user in user.session_users:
        if session_user.session_id == session_id:
            return session_user.session

    raise JsonException('Session not found!', 404)

def create_session(user, session_json):
    if not all(key in session_json for key in ('name', 'start_datetime', 'spot_id')):
        raise JsonException('Missing required fields!', 400)

    new_session = Session(
                          name = session_json['name'],
                          start_datetime = datetime.fromisoformat(session_json['start_datetime']),
                          spot_id = session_json['spot_id']
                          )
    db.session.add(new_session)
    db.session.commit()
    db.session.refresh(new_session)
    
    new_session_user = SessionUser(
                                   session_id=new_session.id,
                                   user_id=user.id
                                   )
    db.session.add(new_session_user)
    db.session.commit()

    db.session.refresh(new_session)
    return new_session

def delete_session(user, session_id):
    for session_user in user.session_users:
        if session_user.session_id == session_id:
            db.session.delete(session_user.session)
            db.session.commit()
            return

    raise JsonException('Session not found!', 404)
    

def modify_session(user, session_id):
    pass

def leave_session(user, session_id):
    for session_user in user.session_users:
        if session_user.session_id == session_id:
            db.session.delete(session_user)
            db.session.commit()
            return

    raise JsonException('Session not found!', 404)

def add_user_to_session(user, session_id, added_user_id):
    added_user = db.session.scalar(db.select(User).where(User.id == added_user_id))
    if not added_user_id:
        raise JsonException('User that you are trying to add does not exist!', 404)

    if session_id not in [session_user.session_id for session_user in user.session_users]:
        raise JsonException('User is not in given session!', 404)
    
    new_session_user = SessionUser(
                                   session_id=session_id,
                                   user_id=added_user_id
                                   )
    db.session.add(new_session_user)
    db.session.commit()

def session_set_parking_loc(user, session_id):
    pass

