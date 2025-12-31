from flask import Blueprint, request, jsonify
from app.services.cart_services import add_item_to_cart, get_cart, remove_item_from_cart, update_item_quantity

cart_bp = Blueprint('cart', __name__, static_folder=None)

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

@cart_bp.get('/user/cart/', strict_slashes=False)
def get_user_cart():
    user_id = request.args.get('user_id')
   
    if not user_id:
        return jsonify({
            'error': True,
            'message': 'Parâmetro user_id é obrigatório.'
        }), 400

    cart, error = get_cart(user_id)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    cart_items = [item.to_dict() for item in getattr(cart, 'items', [])]

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
            'public_id': cart.public_id,
            'items': cart_items
        }
    }), 200
    
@cart_bp.delete('/remove/<int:item_id>')
def remove_from_cart(item_id):
    data = request.get_json()
    user_id = data.get('user_id')

    success, error = remove_item_from_cart(user_id, item_id)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    return jsonify({
        'error': False,
        'message': 'Item removido do carrinho com sucesso!'
    }), 200


@cart_bp.put('/update/<int:item_id>')
def update_cart_item(item_id):
    data = request.get_json()
    user_id = data.get('user_id')
    quantity = data.get('quantity')

    if user_id is None or quantity is None:
        return jsonify({
            'error': True,
            'message': 'Parâmetros user_id e quantity são obrigatórios.'
        }), 400

    cart_item, error = update_item_quantity(user_id, item_id, quantity)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    if cart_item is True:
        return jsonify({
            'error': False,
            'message': 'Item removido do carrinho porque a quantidade é zero ou negativa.'
        }), 200

    return jsonify({
        'error': False,
        'message': 'Quantidade do item atualizada com sucesso!',
        'cart_item': cart_item.to_dict()
    }), 200