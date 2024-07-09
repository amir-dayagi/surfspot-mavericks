from flask import jsonify, request

from ..app import app
from . import controllers
from ..common.utils import token_required, JsonException


@app.route('/groups', methods=['GET'])
@token_required
def get_groups(user) -> '[Group]':
    '''
    Returns all groups a user is a part of
    '''
    groups = controllers.get_groups(user)
    
    response = []
    for group in groups:
        response.append(group.to_dict())
    return jsonify(response), 200

@app.route('/groups', methods=['POST'])
@token_required
def create_group(user) -> 'Group':
    '''
    HTTP Body: {name: <group name>}
    
    Creates a new group and adds user to the session
    '''
    try:
        group = controllers.create_group(user, request.get_json())
        return jsonify(group.to_dict()), 201
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status


@app.route('/groups/<int:group_id>/users', methods=['GET'])
@token_required
def get_group_users(user, group_id) -> '[User]':
    '''
    Returns all users in given group_id that the user is a part of
    '''
    try:
        users = controllers.get_group_users(user, group_id)

        response = []
        for user in users:
            response.append(user.to_dict())
        return jsonify(response), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

@app.route('/groups/<int:group_id>/add/<int:added_user_id>', methods=['PATCH'])
@token_required
def add_to_group(user, group_id, added_user_id):
    '''
    Adds given user to given group if requesting user is in given group and user exsits
    '''
    try:
        controllers.add_to_group(user, group_id, added_user_id)
        return jsonify({'message': f'User with id {added_user_id} added to group with id {group_id}!'}), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

@app.route('/groups/<int:group_id>/start-session', methods=['POST'])
@token_required
def start_session(user, group_id) -> 'Session':
    '''
    HTTP Body: {start_date: <start_date>,
                spot_id: <spot_id>}

    Starts a session in given group with said start date and spot
    '''
    try:
        session = controllers.start_session(user, group_id, request.get_json())
        return jsonify(session.to_dict()), 201
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

@app.route('/groups/<int:group_id>/join-session', methods=['POST'])
@token_required
def join_session(user, group_id) -> None:
    '''
    Joins active session in given group if session exists.
    '''
    try:
        controllers.join_session(user, group_id)
        return jsonify({'message': 'Joined session!'}), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

@app.route('/groups/<int:group_id>/leave-session', methods=['DELETE'])
@token_required
def leave_session(user, group_id) -> None:
    '''
    Leaves active session in given group if session exists and user is in session.
    '''
    try:
        controllers.leave_session(user, group_id)
        return jsonify({'message': 'Left session!'}), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status


@app.route('/groups/<int:group_id>/session-users', methods=['GET'])
@token_required
def get_session_users(user, group_id) -> '[User]':
    '''
    Returns all users that are in the group's active session
    '''
    try:
        users = controllers.get_session_users(user, group_id)
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

    response = []
    for user in users:
        response.append(user.to_dict_with_loc())
    return jsonify(response), 200

@app.route('/groups/<int:group_id>/messages', methods=['GET'])
@token_required
def get_messages(user, group_id) -> 'next_cursors + [Message]':
    cursor = request.args.get('cursor', default=None, type=int)
    limit = request.args.get('limit', default=20, type=int)
    ascending = request.args.get('ascending', default=True, type=lambda x: x.lower()=='true')
    try:
        messages = controllers.get_messages(user, group_id, cursor, limit, ascending)
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status
    
    print(cursor, limit, ascending)
    response = {
        'ascending_next_cursor': messages[-1].id+1 if messages else 0,
        'descending_next_cursor': messages[0].id-1 if messages else 0,
        'messages': [message.to_dict(user.id) for message in messages]
    }
    return jsonify(response), 200

# @app.route('/groups/<int:group_id>/latest-messages', methods=['GET'])
# @token_required
# def get_latest_messages(user, group_id) -> '[Message]':
#     '''
#     Returns latest messages of group up to given limit
#     '''
#     limit = int(request.args.get('limit', default=20))
#     try:
#         messages = controllers.get_latest_messages(user, group_id, limit)
#     except JsonException as e:
#         return jsonify({'message': str(e)}), e.status
    
#     response = []
#     for message in messages:
#         response.append(message.to_dict(user.id))
#     return jsonify(response), 200

@app.route('/groups/<int:group_id>/messages', methods=['POST'])
@token_required
def send_message(user, group_id) -> 'Message':
    '''
    HTTP Body: {context: <message text>}

    Send a message in given group.
    '''
    try:
        message = controllers.send_message(user, group_id, request.get_json())
        return jsonify(message.to_dict(user.id)), 201
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status