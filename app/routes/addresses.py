from flask import Blueprint, request, jsonify
from app.middlewares.auth_middlewares import auth_required
from app.services.address_services import create_address, get_addresses, delete

address_bp = Blueprint('address', __name__)

@address_bp.post('/new')
@auth_required
def create():
    data = request.get_json()
    name = data.get("name")
    long = data.get("long")
    lat = data.get("lat")
    user_id = request.user["sub"]
    
    if not name or not long or not lat:
        return jsonify({
            'error': True,
            'message': 'Alguns campos são obrigatórios.'
        }), 400
        
    try:    
        address = create_address(user_id)
    except:
        return jsonify({
            'error': True,
            'message': 'Erro ao cadastrar endereço.',
        }), 500
        
    return jsonify({
        'error': False,
        'message': 'Endereço cadastrado com sucesso!',
        'address': address.to_dict()
    })

@address_bp.get('/user')
@auth_required
def get_user_addresses():
    user_id = request.user["sub"]
    
    addresses, error = get_addresses(user_id)
    
    print(addresses)
    
    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404
        
    return jsonify({
        'error': False,
        'message': 'Endereços encontrados com sucesso!',
        'addresses': [address.to_dict() for address in addresses]
    })
    
@address_bp.delete('/address/<int:id>')
@auth_required
def remove_address(id):
    deleted, error = delete(id)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 400
    return jsonify({
        'error': False,
        'message': 'Endereço deletado com sucesso.'
    }), 200
