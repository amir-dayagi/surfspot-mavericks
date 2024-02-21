from flask import request

from ..app import app
from . import controllers

@app.route('/sessions', methods=['GET'])
def get_sessions():
    return controllers.get_sessions()


@app.route('/sessions/<int:id>', methods=['GET'])
def get_session(id: int):
    return controllers.get_session(id)


@app.route('/sessions', methods=['POST'])
# @schema.validate(session_schema)
def create_session():
    session = controllers.create_session()
    return session, 201


@app.route('/sessions/<int:id>', methods=['DELETE'])
def delete_session(id: int):
    session = controllers.delete_session(id)
    return session


@app.route('/sessions/<int:session_id>/add-user/<int:user_id>', methods=['PATCH'])
def session_add_user(session_id: int, user_id: int):
    controllers.session_add_user(session_id, user_id)
    return {'status': 204}


@app.route('/sessions/<int:session_id>/remove-user/<int:user_id>', methods=['PATCH'])
def session_remove_user(session_id: int, user_id: int):
    controllers.session_remove_user(session_id, user_id)
    return {'status': 204}


@app.route('/sessions/<int:session_id>/users', methods=['GET'])
def session_get_users(session_id: int):
    return controllers.session_get_users(session_id)


# @app.route('/sessions/<int:session_id>/users/<int:user_id>', methods=['GET'])    
# def session_get_user(session_id: int, user_id: int):
#     return controllers.session_get_user(session_id, user_id)


@app.route('/sessions/<int:session_id>/user-park-loc/<int:user_id>', methods=['PATCH'])
# @schema.validate(location_schema)
def session_set_parking_loc(session_id: int, user_id: int):
    controllers.session_set_parking_loc(session_id, user_id)
    return {'status': 204}


@app.route('/sessions/<int:session_id>/user-surf-loc/<int:user_id>', methods=['PATCH'])
# @schema.validate(location_schema)
def session_set_surfing_loc(session_id: int, user_id: int):
    controllers.session_set_surfing_loc(session_id, user_id)
    return {'status': 204}


# session_schema = {
#     'type': 'object',
#     'definitions': {
#         'area': { # circle around location with a given radius in miles
#             'type': 'object',
#             'properties': {
#                 'longitude': {'type': 'number'},
#                 'latitude': {'type': 'number'},
#                 'radius': {'type': 'number'}
#             },
#             'required': ['longitude', 'latitude', 'radius']
#         }
#     },
#     'properties': {
#         'name': {'type': 'string'},
#         'start_datetime': {'type': 'string'},
#         'end_datetime': {'type': 'string'},
#         'area': {'$ref': '#/definitions/area'}
#     },
#     'required': ['name', 'start_datetime', 'end_datetime', 'area']
# }

# location_schema = {
#     'type': 'object',
#     'properties': {
#         'longitude': {'type': 'number'},
#         'latitude': {'type': 'number'}
#     },
#     'required': ['longitude', 'latitude']
# }

# @app.errorhandler(JsonValidationError)
# def validation_error(e):
#     return jsonify({'error': e.message, 'errors': [validation_error.message for validation_error in e.errors]})
