from flask import Blueprint, request, jsonify
from app.middlewares.auth_middlewares import auth_required, is_admin
from app.services.order_services import create, update_status, get_all, get_orders_by_user_id

order_bp = Blueprint('order', __name__)

@order_bp.post('/order/new')
@auth_required
def create_order():
    data = request.get_json()
    user_id = request.user["sub"]
    items = data.get('items')
    address = data.get('address')
    phone_number = data.get('phone') or data.get('phone_number')
    affiliate_code = data.get('affiliate_code')

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

    if isinstance(address, dict):
        addr_obj = address
    else:
        return jsonify({'error': True, 'message': 'Endereço inválido.'}), 400

    order, error = create(user_id, items, addr_obj, phone_number, affiliate_code)

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
    
@order_bp.get("/user/")
@auth_required
def get_user_orders():
    user_id = request.user["sub"]
    orders = get_orders_by_user_id(user_id)
    
    if not orders:
        return jsonify({
            'error': True,
            'message': 'Nenhum pedido encontrado'
        }), 404
    
    return jsonify({
        'error': False,
        'message': 'Pedidos listados com sucesso!',
        'orders': [order.to_dict() for order in orders]
    })

@order_bp.put('/<int:id>/status')
@auth_required
@is_admin
def update_order_status(id):
    data = request.get_json()
    status = data.get('status')

    if not status:
        return jsonify({
            'error': True,
            'message': 'O campo status é obrigatório.'
        }), 400

    order, error = update_status(id, status)

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

@order_bp.get('/')
def get_all_orders():
    try:
        orders = get_all()
    except:
        return jsonify({
            'error': True,
            'message': 'Erro ao carregar pedidos.'
        }), 500

    if not orders:
        return jsonify({
            'error': True,
            'message': 'Nenhum pedido encontrado.'
        }), 404

    return jsonify({
        'error': False,
        'orders': [order.to_dict() for order in orders],
        'total': len(orders)
    }), 200