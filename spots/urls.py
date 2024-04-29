from flask import jsonify, request

from ..app import app
from . import controllers
from ..common.utils import JsonException


@app.route('/spots', methods=['GET'])
def get_spots():
    '''
    Returns all spots
    '''
    spots = controllers.get_spots()
    
    response = []
    for spot in spots:
        response.append(spot.to_dict())
    return jsonify(response), 200

@app.route('/spots/<int:spot_id>', methods=['GET'])
def get_spot(spot_id):
    '''
    Returns spot with given spot_id
    '''
    try:
        spot = controllers.get_spot(spot_id)
        return jsonify(spot.to_dict()), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

@app.route('/spots', methods=['POST'])
def create_spot():
    '''
    HTTP Body: {name: <session name>,
                latitude: <latitude>
                longitude: <longitude>,
                radius: <radius>}
    
    Creates a new spot
    '''
    try:
        new_spot = controllers.create_spot(request.get_json())
        return jsonify(new_spot.to_dict()), 201
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status

@app.route('/spots/<int:spot_id>', methods=['DELETE'])
def delete_spot(spot_id):
    '''
    Deletes spot with given spot_id
    '''
    try:
        controllers.delete_spot(spot_id)
        return jsonify({'message': 'Spot deleted!'}), 200
    except JsonException as e:
        return jsonify({'message': str(e)}), e.status