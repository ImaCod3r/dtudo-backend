from flask import Blueprint, request, jsonify
from app.services.cart_services import add_item_to_cart, get_cart_details, remove_item_from_cart

cart_bp = Blueprint('cart', __name__)

@cart_bp.post('/add')
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    cart_item, error = add_item_to_cart(user_id, product_id, quantity)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    return jsonify({
        'error': False,
        'message': 'Produto adicionado ao carrinho com sucesso!',
        'cart_item': cart_item.to_dict()
    }), 201

@cart_bp.get('/<string:cart_id>')
def get_cart(cart_id):
    cart, error = get_cart(cart_id)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    cart_items = [item.to_dict() for item in cart.items]

    if not cart_items:
        return jsonify({
            'error': False,
            'message': 'Carrinho vazio.',
            'cart': None
        }), 200

    return jsonify({
        'error': False,
        'message': 'Carrinho recuperado com sucesso!',
        'cart': {
            'id': cart.id,
            'public_id': cart.public_id,
            'items': cart_items
        }
    }), 200 
    
@cart_bp.delete('/remove/<int:product_id>')
def remove_from_cart(product_id):
    data = request.get_json()
    user_id = data.get('user_id')

    success, error = remove_item_from_cart(user_id, product_id)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    return jsonify({
        'error': False,
        'message': 'Item removido do carrinho com sucesso!'
    }), 200