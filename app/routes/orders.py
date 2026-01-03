from flask import Blueprint, request, jsonify
from app.middlewares.auth_middlewares import auth_required
from app.services.order_services import create_order, update_order_status
order_bp = Blueprint('order', __name__)

@order_bp.post('/order/new')
@auth_required
def create_order_route():
    data = request.get_json()
    user_id = request.user["sub"]
    items = data.get('items')
    address = data.get('address')
    phone_number = data.get('phone') or data.get('phone_number')

    if not phone_number:
        return jsonify({
            'error': True,
            'message': 'O número de telefone é obrigatório.'
        }), 400

    if not items:
        return jsonify({
            'error': True,
            'message': 'O carrinho está vazio.'
        }), 400

    if not address:
        return jsonify({
            'error': True,
            'message': 'O endereço é obrigatório.'
        }), 400

    # address is expected to be an object with name, long, lat
    if isinstance(address, dict):
        addr_obj = address
    else:
        return jsonify({'error': True, 'message': 'Endereço inválido.'}), 400

    order, error = create_order(user_id, items, addr_obj, phone_number)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 400

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