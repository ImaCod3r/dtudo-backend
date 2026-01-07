from app.models.order import Order
from app.models.orderItem import OrderItem
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart
from app.models.cartItem import CartItem
from app.services.address_services import create_address
from app.services.notification_services import send_notification_to_admins, send_notification_to_user

SHIPPING_FEE = 2000.0

def get_all():
    return Order.select()

def get_orders_by_user_id(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return []
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

def create(user_id, items, address, phone_number, affiliate_code=None):
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
            total_price=0.0,
            affiliate_code=affiliate_code
        )
    except: 
        return None, "Erro ao enviar pedido!"

    total = SHIPPING_FEE

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
            price=product.price,
            affiliate_code=it.get('affiliate_code')
        )
        total += quantity * product.price

    order.total_price = total
    order.save()

    try:
        send_notification_to_admins({
            "title": "Novo Pedido Recebido! 🛍️",
            "body": f"Pedido #{order.id} - Total: Kz {order.total_price:,.2f}",
            "url": "/pedidos"
        })
    except Exception as e:
        print(f"Failed to send notification: {e}")

    # Limpar carrinho do usuário
    try:
        cart = Cart.get_or_none(Cart.user == user)
        if cart:
            CartItem.delete().where(CartItem.cart == cart).execute()
    except Exception as e:
        print(f"Erro ao limpar carrinho: {e}")


    return order, None

def update_status(order_id, new_status):
    valid_statuses = ['Pendente', 'Confirmado', 'Entregue', 'Cancelado']
    if new_status not in valid_statuses:
        return None, "Status inválido."

    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return None, "Pedido não encontrado."

    old_status = order.status
    order.status = new_status
    order.save()

    # Enviar notificação ao cliente sobre a mudança de status
    if old_status != new_status:
        status_messages = {
            'Confirmado': {
                'title': 'Pedido Confirmado! ✅',
                'body': f'Seu pedido #{order.id} foi confirmado e está sendo preparado.',
                'url': '/perfil'
            },
            'Entregue': {
                'title': 'Pedido Entregue! 🎉',
                'body': f'Seu pedido #{order.id} foi entregue com sucesso. Obrigado!',
                'url': '/perfil'
            },
            'Cancelado': {
                'title': 'Pedido Cancelado ❌',
                'body': f'Seu pedido #{order.id} foi cancelado.',
                'url': '/perfil'
            }
        }
        
        if new_status in status_messages:
            try:
                send_notification_to_user(order.user.id, status_messages[new_status])
            except Exception as e:
                print(f"Failed to send notification to user: {e}")

    if new_status == 'Entregue':
        from app.services.affiliate_services import calculate_commissions_for_order
        calculate_commissions_for_order(order)

    return order, None