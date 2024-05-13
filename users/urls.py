from flask import jsonify, request

from ..app import app
from . import controllers
from ..common.utils import JsonException


@app.route('/users', methods=['GET'])
def get_users():
    '''
    Returns all users including search query
    '''
    search_query = request.args.get('name')
    users = controllers.get_users(search_query)
    
    response = []
    for user in users:
        response.append(user.to_dict())
    return jsonify(response), 200
