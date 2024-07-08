from flask import jsonify, request

from ..app import app
from . import controllers
from ..common.utils import token_required, JsonException


@app.route('/users', methods=['GET'])
def get_users() -> '[User]':
    '''
    Returns all users including search query
    '''
    search_query = request.args.get('query', default='')
    limit = int(request.args.get('limit', default=10))
    users = controllers.get_users(search_query, limit)
    
    response = []
    for user in users:
        response.append(user.to_dict())
    return jsonify(response), 200

@app.route('/users/update-location', methods=['PATCH'])
@token_required
def update_location(user) -> None:
    try:
        controllers.update_location(user, request.get_json())
        return jsonify({'message': 'Location updated successfully!'}), 201
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status