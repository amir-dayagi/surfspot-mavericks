from flask import request, jsonify
from .. import db
from .models import User

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
                    name=user_json['name'],
                    email=user_json['email']
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

