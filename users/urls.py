from flask import request

from ..app import app
from . import controllers

@app.route('/users', methods=['GET'])
def get_users():
    return controllers.get_users()


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id: int):
    return controllers.get_user(id)


@app.route('/users', methods=['POST'])
# @schema.validate(user_schema)
def create_user():
    user = controllers.create_user()
    return user, 201


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    user = controllers.delete_user(id)
    return user 


@app.route('/users/<int:user_id>/sessions', methods=['GET'])
def user_get_sessions(user_id: int):
    return controllers.user_get_sessions(user_id)


# @app.route('/users/<int:user_id>/sessions/<int:session_id>', methods=['GET'])
# def user_get_session(user_id: int, session_id: int):
#     return controllers.user_get_session(user_id, session_id)



# user_schema = {
#     'type': 'object',
#     'properties': {
#         'name': {'type': 'string'},
#         'email': {'type': 'string'},
#     },
#     'required': ['name', 'email']
# }