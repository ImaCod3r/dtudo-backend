from flask import Blueprint, request, jsonify
from app.services.order_services import create_order, update_order_status
from app.models.user import User

order_bp = Blueprint('order', __name__)

@order_bp.post('/create')
def create_order_route():
    data = request.get_json()
    user_id = data.get('user_id')
    phone = data.get('phone')
    address = data.get('address')

    user = User.get_or_none(User.public_id == user_id)
    if not user:
        return jsonify({
            'error': True,
            'message': 'Usuário não encontrado.'
        }), 404

    order, error = create_order(user, phone, address)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    return jsonify({
        'error': False,
        'message': 'Pedido criado com sucesso!',
        'order': order.to_dict()
    }), 201

@order_bp.patch('/<order_id>/status')
def update_order_status_route(order_id):
    data = request.get_json()
    status = data.get('status')

    if not status:
        return jsonify({
            'error': True,
            'message': 'O campo status é obrigatório.'
        }), 400

    order, error = update_order_status(order_id, status)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 400

    return jsonify({
        'error': False,
        'message': 'Status do pedido atualizado com sucesso!',
        'order': order.to_dict()
    }), 200