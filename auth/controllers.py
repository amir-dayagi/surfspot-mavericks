from datetime import datetime, timedelta
import jwt
import os
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from ..app import app
from ..sessions.models import Session
from ..common.models import User, SessionUser
from ..common.utils import JsonException

def login(login_json):
    if not all(key in login_json for key in ('email', 'password')):
        raise JsonException('Missing required fields!', 401)
    
    user = db.session.scalar(db.select(User).where(User.email == login_json['email']))
    if not user:
        raise JsonException('User does not exist!', 401)
    
    if not check_password_hash(user.password, login_json['password']):
        raise JsonException('Wrong password!', 403)
    
    token = jwt.encode({
                        'id': user.id,
                        'exp': datetime.now() + timedelta(weeks=1)
                        }, app.config['SECRET_KEY'], "HS256")
    
    return token


def signup(signup_json):
    if not all(key in signup_json for key in ('email', 'password', 'first_name')):
        raise JsonException('Missing required fields!', 400)
    
    user = db.session.scalar(db.select(User).where(User.email == signup_json['email']))
    if user:
        raise JsonException('User with email already exists!', 400)
    
    user = User(
                email = signup_json['email'],
                password = generate_password_hash(signup_json['password']),
                first_name = signup_json['first_name']
                )
    
    if 'last_name' in signup_json: user.last_name = signup_json['last_name']

    db.session.add(user)
    db.session.commit()
