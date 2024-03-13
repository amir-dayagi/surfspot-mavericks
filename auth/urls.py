from flask import jsonify, request

from ..app import app
from . import controllers
from ..common.utils import JsonException

@app.route('/login', methods=['POST'])
def login():
    try:
        token = controllers.login(request.get_json())
        return jsonify({'token': token}), 200
    except JsonException as e:
        return jsonify({'message': e.message}), e.status


@app.route('/signup', methods=['POST'])
def signup():
    try:
        controllers.signup(request.get_json())
        return jsonify({'message': 'Account created successfully!'}), 201
    except JsonException as e:
        return jsonify({'message': e.message}), e.status

    

