from flask import request

from ..app import app
from . import controllers
from ..common.utils import token_required


@app.route('/sessions', methods=['GET'])
@token_required
def get_sessions(user):
    return controllers.get_sessions(user)

# @app.route('/sessions/<int:session_id>', methods=['GET'])
# @token_required
# def get_session(user, session_id):
#     return controllers.get_session(user, session_id)


@app.route('/sessions/', methods=['POST'])
@token_required
def create_session(user):
    return controllers.create_session(user)

# @app.route('/sessions/<int:session_id>', methods=['DELETE'])
# @token_required
# def delete_session(user, session_id):
#     return controllers.delete_session(user, session_id)

# @app.route('/sessions/<int:session_id>', methods=['PATCH'])
# @token_required
# def modify_session(user, session_id):
#     return controllers.modify_session(user, session_id)


# @app.route('/sessions/<int:session_id>/leave', methods=['PATCH'])
# @token_required
# def leave_session(user, session_id):
#     return controllers.leave_session(user, session_id)

# @app.route('/sessions/<int:session_id>/add-user/<int:added_user_id>', methods=['PATCH'])
# @token_required
# def add_user_to_session(user, session_id, added_user_id):
#     return controllers.add_user_to_session(user, session_id, adding_user_id)


# @app.route('/sessions/<int:session_id>/user-park-loc/', methods=['PATCH'])
# @token_required
# def session_set_parking_loc(session_id: int, user_id: int):
#     return controllers.session_set_parking_loc(user, session_id)

