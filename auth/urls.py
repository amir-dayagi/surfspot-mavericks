from flask import jsonify, request

from ..app import app
from . import controllers
from ..common.utils import JsonException

@app.route('/login', methods=['POST'])
def login():
    '''
    HTTP Body: {email: <user email>,
                password: <user password>}
    
    Validates that user with email and password exist and returns a token and its expiration date.
    '''
    try:
        token, exp = controllers.login(request.get_json())
        return jsonify({'token': token, 'exp': exp.replace(microsecond=0).isoformat()}), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status



@app.route('/signup', methods=['POST'])
def signup():
    '''
    HTTP Body: {email: <user email>,
                password: <user password>,
                first_name: <user first name>
                last_name: <optional! user last_name>}

    Creates a new account if user with email doesn't already exist
    '''
    try:
        controllers.signup(request.get_json())
        return jsonify({'message': 'Account created successfully!'}), 201
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

    

