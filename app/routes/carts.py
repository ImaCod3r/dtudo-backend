from flask import Blueprint, request, jsonify
from app.middlewares.auth_middlewares import auth_required
from app.services.cart_services import add_item, get, remove_item, update_item_quantity, clear

cart_bp = Blueprint('cart', __name__, static_folder=None)

@cart_bp.post('/add')
@auth_required
def add_to_cart():
    data = request.get_json()
    user_id = request.user["sub"]
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    cart_item, error = add_item(user_id, product_id, quantity)

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
@auth_required
def get_user_cart():
    user_id = request.user["sub"]

    if not user_id:
        return jsonify({
            'error': True,
            'message': 'Parâmetro user_id é obrigatório.'
        }), 400

    cart, error = get(user_id)

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
@auth_required
def remove_from_cart(item_id):
    user_id = request.user["sub"]
    _, error = remove_item(user_id, item_id)
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
@auth_required
def update_cart_item(item_id):
    data = request.get_json()
    user_id = request.user["sub"]
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

@cart_bp.delete('/clear')
@auth_required
def clear_cart():
    user_id = request.user["sub"]
    _, error = clear(user_id)
    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    return jsonify({
        'error': False,
        'message': 'Carrinho limpo com sucesso!'
    }), 200