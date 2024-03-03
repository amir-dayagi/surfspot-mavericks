from datetime import datetime

from flask import request, jsonify
from .. import db
from .models import Session
from ..users.models import User
from ..session_users.models import SessionUser

def get_sessions():
    sessions = db.session().scalars(db.select(Session))
    response = []
    for session in sessions:
        response.append(session.to_dict())
    return jsonify(response)


def get_session(id: int):
    response = db.session.scalar(db.select(Session).where(Session.id == id))
    return jsonify(response.to_dict())


def create_session():
    def get_area(session_json):
        return session_json['area']
    
    def get_datetime(datetime_str):
        return datetime.now()
    
    session_json = request.get_json()
    new_session = Session(
                          name = session_json['name'],
                          start_datetime = get_datetime(session_json['start_datetime']),
                          end_datetime = get_datetime(session_json['end_datetime']),
                          area = get_area(session_json)
                          )
    db.session.add(new_session)
    db.session.commit()
    db.session.refresh(new_session)
    return jsonify(new_session.to_dict())


def delete_session(id: int):
    session_to_delete = db.session.scalar(db.select(Session).where(Session.id == id))
    db.session.delete(session_to_delete)
    db.session.commit()
    return jsonify(session_to_delete.to_dict())


def session_add_user(session_id: int, user_id: int):
    new_session_user = SessionUser(
                                   session_id=session_id,
                                   user_id=user_id
                                   )
    db.session.add(new_session_user)
    db.session.commit()


def session_remove_user(session_id: int, user_id: int):
    session_user_to_delete = db.session.scalar(db.select(SessionUser)
                                                 .where(SessionUser.session_id == session_id)
                                                 .where(SessionUser.user_id == user_id)
                                               )
    db.session.delete(session_user_to_delete)
    db.session.commit()


def session_get_users(session_id: int):
    users = db.session().scalars(db.select(User)
                                   .where(User.session_users.any(SessionUser.session_id == session_id))
                                 )
    response = []
    for user in users:
        response.append(user.to_dict())
    return jsonify(response)


def session_get_user(session_id: int, user_id: int):
    session_user = db.session().scalar(db.select(SessionUser)
                                    .where(SessionUser.session_id == session_id)
                                    .where(SessionUser.user_id == user_id))
    return jsonify(session_user.user.to_dict())


def session_set_parking_loc(session_id: int, user_id: int):
    location_json = request.get_json()
    session_user = db.session.scalar(db.select(SessionUser)
                                        .where(SessionUser.session_id == session_id)
                                        .where(SessionUser.user_id == user_id)
                                     )
    session_user.parking_location = location_json['parking_location']
    db.session.commit()


def session_set_surfing_loc(session_id: int, user_id: int):
    location_json = request.get_json()
    session_user = db.session.scalar(db.select(SessionUser)
                                        .where(SessionUser.session_id == session_id)
                                        .where(SessionUser.user_id == user_id)
                                    )
    session_user.surfing_location = location_json['surfing_location']
    db.session.commit()