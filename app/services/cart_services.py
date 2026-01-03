from app.models.cart import Cart
from app.models.cartItem import CartItem
from app.models.product import Product
from app.models.user import User

def add_item(user_id, product_id, quantity=1):
    user = User.get_or_none(User.id == user_id)
    cart, created = Cart.get_or_create(user=user)

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

def get(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return None, "Usuário não encontrado."

    cart = Cart.get_or_none(Cart.user == user)
    
    if not cart:
        return None, "Carrinho não encontrado."

    return cart, None

def remove_item(user_id, item_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return None, "Usuário não encontrado."

    cart = Cart.get_or_none(Cart.user == user)
    
    if not cart:
        return None, "Carrinho não encontrado."

    cart_item = CartItem.get_or_none(CartItem.cart == cart, CartItem.id == item_id)
    if not cart_item:
        return None, "Item do carrinho não encontrado."

    cart_item.delete_instance()
    
    return True, None

def update_item_quantity(user_id, item_id, quantity):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return None, "Usuário não encontrado."

    cart = Cart.get_or_none(Cart.user == user)
    if not cart:
        return None, "Carrinho não encontrado."

    cart_item = CartItem.get_or_none(CartItem.cart == cart, CartItem.id == item_id)
    if not cart_item:
        return None, "Item do carrinho não encontrado."

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return None, "Quantidade inválida."

    if quantity <= 0:
        cart_item.delete_instance()
        return True, None

    cart_item.quantity = quantity
    cart_item.save()

    return cart_item, None

def clear(user_id):
    user = User.get_or_none(User.id == user_id)

    cart = Cart.get_or_none(Cart.user == user)
    if not cart:
        return None, "Carrinho não encontrado."

    cart.items.clear()
    cart.save()

    return True, None