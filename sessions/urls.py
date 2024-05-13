from flask import jsonify, request

from ..app import app
from . import controllers
from ..common.utils import token_required, JsonException


@app.route('/sessions', methods=['GET'])
@token_required
def get_sessions(user):
    '''
    Returns all sessions a user is a part of
    '''
    sessions = controllers.get_sessions(user)
    
    response = []
    for session in sessions:
        response.append(session.to_dict())
    return jsonify(response), 200

@app.route('/sessions/<int:session_id>', methods=['GET'])
@token_required
def get_session(user, session_id):
    '''
    Returns session with given session_id that the user is a part of
    '''
    try:
        session = controllers.get_session(user, session_id)
        return jsonify(session.to_dict()), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status



@app.route('/sessions', methods=['POST'])
@token_required
def create_session(user):
    '''
    HTTP Body: {name: <session name>,
                start_datetime: <session start time>,
                spot_id: <spot_id>}
    
    Creates a new session and adds user to the session
    '''
    try:
        session = controllers.create_session(user, request.get_json())
        return jsonify(session.to_dict()), 201
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
@token_required
def delete_session(user, session_id):
    '''
    Deletes sessions with given session_id that the user is a part of
    '''
    try:
        controllers.delete_session(user, session_id)
        return jsonify({'message': 'Session deleted!'}), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

# @app.route('/sessions/<int:session_id>', methods=['PATCH'])
# @token_required
# def modify_session(user, session_id):
#     return controllers.modify_session(user, session_id)


@app.route('/sessions/<int:session_id>/leave', methods=['PATCH'])
@token_required
def leave_session(user, session_id):
    '''
    Removes user from session with given session_id that the user is a part of
    '''
    try:
        controllers.leave_session(user, session_id)
        return jsonify({'message': 'User left session!'}), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

@app.route('/sessions/<int:session_id>/add-user/<int:added_user_id>', methods=['PATCH'])
@token_required
def add_user_to_session(user, session_id, added_user_id):
    return controllers.add_user_to_session(user, session_id, added_user_id)


# @app.route('/sessions/<int:session_id>/user-park-loc/', methods=['PATCH'])
# @token_required
# def session_set_parking_loc(session_id: int, user_id: int):
#     return controllers.session_set_parking_loc(user, session_id)

