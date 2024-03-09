from flask import request, jsonify
from functools import wraps
import jwt
import os

from .. import db
from ..auth.models import User


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not 'Authorization' in request.headers:
            return jsonify({'message': 'Token required!'}), 401
        
        auth_split = request.headers['Authorization'].split(' ')
        if len(auth_split) != 2 or auth_split[0] != 'Bearer':
            return jsonify({'message': 'Token required!'}), 401
        
        token = auth_split[1]
        payload = None
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        
        user = db.session.scalar(db.select(User).where(User.id == payload['id']))
        
        return func(user, *args, **kwargs)
    
    return decorated