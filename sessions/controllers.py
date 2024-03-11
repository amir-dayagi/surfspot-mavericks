from datetime import datetime

from flask import request, jsonify

from .. import db
from .models import Session
from ..auth.models import User
from ..common.models import SessionUser


def get_sessions(user):
    response = []
    for session_user in user.session_users:
        response.append(session_user.session.to_dict())
    return jsonify(response), 200

def get_session(user, session_id):
    for session_user in user.session_users:
        if session_user.session_id == session_id:
            return jsonify(session_user.session.to_dict()), 200
    return jsonify({'message': 'Session not found!'}), 404

def create_session(user):
    session_json = request.get_json()

    if not all(key in session_json for key in ('name', 'start_datetime', 'area')):
        return jsonify({'message': 'Missing required fields!'}), 400

    new_session = Session(
                          name = session_json['name'],
                          start_datetime = datetime.fromisoformat(session_json['start_datetime']),
                          area = session_json['area'] # just text for now!
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
    return jsonify({'message': 'Successfully created session!'}), 201

def delete_session(user, session_id):
    for session_user in user.session_users:
        if session_user.session_id == session_id:
            db.session.delete(session_user.session)
            db.session.commit()
            return jsonify({'message': 'Session deleted!'}), 200
    return jsonify({'message': 'Session not found!'}), 404
    

def modify_session(user, session_id):
    pass

def leave_session(user, session_id):
    for session_user in user.session_users:
        if session_user.session_id == session_id:
            db.session.delete(session_user)
            db.session.commit()
            return jsonify({'message': 'User left session!'}), 200
    return jsonify({'message': 'Session not found!'}), 404

def add_user_to_session(user, session_id, adding_user_id):
    pass

def session_set_parking_loc(user, session_id):
    pass


# def session_add_user(session_id: int, user_id: int):
#     new_session_user = SessionUser(
#                                    session_id=session_id,
#                                    user_id=user_id
#                                    )
#     db.session.add(new_session_user)
#     db.session.commit()



# def session_set_parking_loc(session_id: int, user_id: int):
#     location_json = request.get_json()
#     session_user = db.session.scalar(db.select(SessionUser)
#                                         .where(SessionUser.session_id == session_id)
#                                         .where(SessionUser.user_id == user_id)
#                                      )
#     session_user.parking_location = location_json['parking_location'] # just text for now!
#     db.session.commit()

