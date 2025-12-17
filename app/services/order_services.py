from app.models.order import Order
from app.models.order_item import OrderItem
from app.services.cart_service import create_cart
from app.database import db

def create_order(user, phone, address):
    cart = create_cart(user)
    if not cart.items.exists():
        raise ValueError("Carrinho vazio");

    with db.atomic():
        order = Order.create(
            user=user,
            phone_number=phone,
            address=address
        )

        total = 0
        for item in cart.items:
            OrderItem.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total += item.quantity * item.product.price

        order.total = total
        order.save()
        cart.items.delete()

    return order

def update_order_status(order_public_id, new_status):
    print(new_status)
    valid_statuses = ['pending', 'shipped', 'canceled']
    if new_status not in valid_statuses:
        return None, "Status inválido."

    order = Order.get_or_none(Order.public_id == order_public_id)

    if not order:
        return None, "Pedido não encontrado."

    order.status = new_status
    order.save()

    return order, None