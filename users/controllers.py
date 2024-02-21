from flask import request, jsonify
from .. import db
from .models import User
from ..sessions.models import Session
from ..session_users.models import SessionUser

def get_users():
    users = db.session.scalars(db.select(User))
    response = []
    for user in users:
        response.append(user.to_dict())
    return jsonify(response)


def get_user(id: int):
    response = db.session.scalar(db.select(User).where(User.id == id))
    return jsonify(response.to_dict())


def create_user():
    user_json = request.get_json()
    new_user = User(
                    email      = user_json['email'],
                    first_name = user_json['first_name'],
                    last_name  = user_json['last_name']
                    )
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)
    return jsonify(new_user.to_dict())


def delete_user(id: int):
    user_to_delete = db.session.scalar(db.select(User).where(User.id == id))
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify(user_to_delete.to_dict())


def user_get_sessions(user_id: int):
    sessions = db.session().scalars(db.select(Session)
                                      .where(Session.session_users.any(SessionUser.user_id == user_id)))
    response = []
    for session in sessions:
        response.append(session.to_dict())
    return jsonify(response)


# def user_get_session(user_id: int, session_id: int):
#     session = db.session().scalar(db.select(Session)
#                                     .where(Session.session_users.any(SessionUser.user_id == user_id and SessionUser.session_id == session_id)))
#     return jsonify(session.to_dict())