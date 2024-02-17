from flask import Blueprint

from . import controllers

bp = Blueprint('routes', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    return controllers.get_users()

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id: int):
    return controllers.get_user(id)

@bp.route('/users', methods=['POST'])
# @schema.validate(user_schema)
def create_user():
    user = controllers.create_user()
    return user, 201

@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    user = controllers.delete_user(id)
    return user 

# @bp.route('/users/<int:id>/sessions', methods=['GET'])
# def get_sessions_by_user(id: int):
#     return 200, user.get_sessions(id)



# user_schema = {
#     'type': 'object',
#     'properties': {
#         'name': {'type': 'string'},
#         'email': {'type': 'string'},
#     },
#     'required': ['name', 'email']
# }