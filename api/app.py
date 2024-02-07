from flask import Flask, jsonify, request
from flask_json_schema import JsonSchema, JsonValidationError
import users_services
import sessions_services

app = Flask(__name__)
schema = JsonSchema(app)

user_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
    },
    'required': ['name', 'email']
}

session_schema = {
    'type': 'object',
    'definitions': {
        'area': { # circle around location with a given radius in miles
            'type': 'object',
            'properties': {
                'longitude': {'type': 'number'},
                'latitude': {'type': 'number'},
                'radius': {'type': 'number'}
            },
            'required': ['longitude', 'latitude', 'radius']
        }
    },
    'properties': {
        'name': {'type': 'string'},
        'start_datetime': {'type': 'string'},
        'end_datetime': {'type': 'string'},
        'area': {'$ref': '#/definitions/area'}
    },
    'required': ['name', 'start_datetime', 'end_datetime', 'area']
}

location_schema = {
    'type': 'object',
    'properties': {
        'longitude': {'type': 'number'},
        'latitude': {'type': 'number'}
    },
    'required': ['longitude', 'latitude']
}

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({'error': e.message, 'errors': [validation_error.message for validation_error in e.errors]})


@app.route('/users', methods=['GET'])
def get_users():
    return 200, users.get_users()

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id: int):
    return 200, users.get_user(id)

@app.route('/users', methods=['POST'])
@schema.validate(user_schema)
def create_user():
    user = users.create_user(request.get_json())
    return 201, user

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    user = user.delete_user(id)
    return 200, user 

@app.route('/users/<int:id>/sessions', methods=['GET'])
def get_sessions_by_user(id: int):
    return 200, user.get_sessions(id)


@app.route('/sessions', methods=['GET'])
def get_sessions():
    return 200, sessions.get_sessions()

@app.route('/sessions/<int:id>', methods=['GET'])
def get_session(id: int):
    return 200, sessions.get_session(id)

@app.route('/sessions', methods=['POST'])
@schema.validate(session_schema)
def create_session():
    session = sessions.create_session(request.get_json())
    return 201, session

@app.route('/sessions/<int:id>', methods=['DELETE'])
def delete_session(id: int):
    session = sessions.delete_session(id)
    return 200, session

@app.route('/sessions/<int:session_id>/add-user/<int:user_id>', methods=['PATCH'])
def session_add_user(session_id: int, user_id: int):
    sessions.add_user(session_id, user_id)
    return 204

@app.route('/sessions/<int:session_id>/remove-user/<int:user_id>', methods=['PATCH'])
def session_remove_user(session_id: int, user_id: int):
    sessions.remove_user(session_id, user_id)
    return 204

@app.route('/sessions/<int:session_id>/user-park-loc/<int:user_id>', methods=['PATCH'])
@schema.validate(location_schema)
def session_set_parking_loc(session_id: int, user_id: int):
    sessions.set_parking_loc(session_id, user_id, request.get_json())
    return 204

@app.route('/sessions/<int:session_id>/user-surf-loc/<int:user_id>', methods=['PATCH'])
@schema.validate(location_schema)
def session_set_surf_loc(session_id: int, user_id: int):
    sessions.set_surf_loc(session_id, user_id, request.get_json())
    return 204
