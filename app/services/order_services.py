from app.models.order import Order
from app.models.orderItem import OrderItem
from app.models.user import User
from app.models.product import Product
from app.services.address_services import create_address

def get_all():
    return Order.select()

def get_orders_by_user_id(user_id):
    user = User.get_by_id(user_id)
    return user.orders

def _lookup_product_from_payload(prod_payload):
    if not prod_payload:
        return None
    public_id = prod_payload.get('public_id') or prod_payload.get('publicId')
    if public_id:
        return Product.get_or_none(Product.public_id == public_id)

    prod_id = prod_payload.get('id')
    if prod_id:
        return Product.get_or_none(Product.id == prod_id)

    return None

def create(user_id, items, address, phone_number):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return None, "Usuário não encontrado."

    addr = create_address(user_id, address.get('name'), address.get('long'), address.get('lat'))
    if not addr:
        return None, "Endereço inválido ou usuário não encontrado."

    try:
        order = Order.create(
            user=user,
            phone_number=phone_number,
            address_id=addr.id,
            total_price=0.0
        )
    except: 
        return None, "Erro ao enviar pedido!"

    total = 0.0

    for it in items:
        prod_payload = it.get('product')
        quantity = it.get('quantity', 1)
        product = _lookup_product_from_payload(prod_payload)
        if not product:
            order.delete_instance(recursive=True)
            return None, f"Produto não encontrado para item: {prod_payload}"

        OrderItem.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        total += quantity * product.price

    order.total_price = total
    order.save()

    return order, None

def update_status(order_id, new_status):
    valid_statuses = ['Pendente', 'Confirmado', 'Entregue', 'Cancelado']
    if new_status not in valid_statuses:
        return None, "Status inválido."

    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return None, "Pedido não encontrado."

    order.status = new_status
    order.save()

    return order, None