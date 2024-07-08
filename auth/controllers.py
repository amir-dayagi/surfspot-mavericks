from datetime import datetime, timedelta
import jwt
import os
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from ..app import app
from ..common.models import User
from ..common.utils import JsonException

def login(login_request) -> '(token, exp)':
    if not all(key in login_request for key in ('username', 'password')):
        raise JsonException('Missing required fields!', 401)
    
    user = db.session.scalar(db.select(User).where(User.username == login_request['username']))
    if not user:
        raise JsonException('User does not exist!', 401)
    
    if not check_password_hash(user.password, login_request['password']):
        raise JsonException('Wrong password!', 403)
    
    exp = datetime.now() + timedelta(weeks=1)
    token = jwt.encode({
                        'id': user.id,
                        'exp': exp
                        }, app.config['SECRET_KEY'], "HS256")
    
    return token, exp


def signup(signup_request) -> None:
    if not all(key in signup_request for key in ('username', 'password')):
        raise JsonException('Missing required fields!', 401)
    
    user = db.session.scalar(db.select(User).where(User.username == signup_request['username']))
    if user:
        raise JsonException('User with username already exists!', 400)
    
    user = User(
                username = signup_request['username'],
                password = generate_password_hash(signup_request['password'])
                )

    db.session.add(user)
    db.session.commit()
