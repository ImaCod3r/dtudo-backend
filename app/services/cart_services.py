from app.models.cart import Cart
from app.models.cartItem import CartItem
from app.models.product import Product
from app.models.user import User
from app.utils.generate_public_id import generate_public_id

def add_item_to_cart(user_public_id, product_id, quantity=1):
    user = User.get_or_none(User.public_id == user_public_id)
    if not user:
        return None, "Usuário não encontrado."
    
    cart, created = Cart.get_or_create(user=user, defaults={'public_id': generate_public_id('cart')})

    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return None, "Produto não encontrado."

    cart_item, item_created = CartItem.get_or_create(
        cart=cart, 
        product=product, 
        defaults={'quantity': quantity}
    )
    
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    return cart_item, None

def get_cart_details(cart_public_id):
    cart = Cart.get_or_none(Cart.public_id == cart_public_id)
    if not cart:
        return None, "Carrinho não encontrado."
    
    return cart, None

def remove_item_from_cart(user_public_id, product_id):
    user = User.get_or_none(User.public_id == user_public_id)
    if not user:
        return None, "Usuário não encontrado."

    cart = Cart.get_or_none(Cart.user == user)
    if not cart:
        return None, "Carrinho não encontrado."

    cart_item = CartItem.get_or_none(CartItem.cart == cart, CartItem.product == product_id)
    if not cart_item:
        return None, "Item do carrinho não encontrado."

    cart_item.delete_instance()
    
    return True, None
