from flask import Blueprint, request, jsonify
from app.models.cart import Cart
from app.models.cartItem import CartItem
from app.models.product import Product
from app.models.user import User
from app.utils.generate_public_id import generate_public_id

cart_bp = Blueprint('cart', __name__)

@cart_bp.post('/add')
def add_to_cart():
    data = request.get_json()
    user = User.get_or_none(User.public_id == data.get('user_id'))
    if not user:
        return jsonify({
            'error': True,
            'message': 'Usuário não encontrado.'
        }), 404

    cart, created = Cart.get_or_create(user=user, defaults={'public_id': generate_public_id('cart')})

    product = Product.get_or_none(Product.id == data.get('product_id'))
    if not product:
        return jsonify({
            'error': True,
            'message': 'Produto não encontrado.'
        }), 404

    cart_item, item_created = CartItem.get_or_create(cart=cart, product=product, defaults={'quantity': data.get('quantity', 1)})
    if not item_created:
        cart_item.quantity += data.get('quantity', 1)
        cart_item.save()

    return jsonify({
        'error': False,
        'message': 'Produto adicionado ao carrinho com sucesso!',
        'cart_item': cart_item.to_dict()
    }), 201

@cart_bp.get('/<str:cart_id>')
def get_cart(cart_id):
    cart = Cart.get_or_none(Cart.public_id == cart_id)
    if not cart:
        return jsonify({
            'error': True,
            'message': 'Carrinho não encontrado.'
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
    user = User.get_or_none(User.public_id == data.get('user_id'))
    if not user:
        return jsonify({
            'error': True,
            'message': 'Usuário não encontrado.'
        }), 404

    cart = Cart.get_or_none(Cart.user == user)

    if not cart:
        return jsonify({
            'error': True,
            'message': 'Carrinho não encontrado.'
        }), 404

    cart_item = CartItem.get_or_none(CartItem.cart == cart, CartItem.product == product_id)
    if not cart_item:
        return jsonify({
            'error': True,
            'message': 'Item do carrinho não encontrado.'
        }), 404

    cart_item.delete_instance()

    return jsonify({
        'error': False,
        'message': 'Item removido do carrinho com sucesso!'
    }), 200