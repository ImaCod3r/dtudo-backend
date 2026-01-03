from flask import Blueprint, request, jsonify

address_bp = Blueprint('address', __name__)

@address_bp.post('/addresses')
def create_address():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    long = data.get('long')
    lat = data.get('lat')

    address = create_address(user_id, name, long, lat)
    if not address:
        return jsonify({"error": "Failed to create address"}), 400

    return jsonify({"address": address}), 201