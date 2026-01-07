# Models
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.cart import Cart
from app.models.address import Address
from app.models.orderItem import OrderItem
from app.models.cartItem import CartItem
from app.models.image import Image
from app.models.log import Log
from app.models.push_subscription import PushSubscription


from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_IN = (60 * 60 * 24) * 7  # 7 dias

def config_database(db):
    db.connect()
    db.create_tables([User, Category, Product, Order, Cart, OrderItem, CartItem, Image, Address, Log, PushSubscription])


    return db

def config_routes(app):
    # Routes - Imported here to avoid circular dependencies
    from app.routes.products import products_bp
    from app.routes.categories import categories_bp  
    from app.routes.carts import cart_bp  
    from app.routes.auth import auth_bp
    from app.routes.orders import order_bp
    from app.routes.addresses import address_bp
    from app.routes.users import users_bp
    from app.routes.logs import logs_bp
    from app.routes.images import images_bp
    from app.routes.notifications import notifications_bp



    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(cart_bp, url_prefix='/carts')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(address_bp, url_prefix='/addresses')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(logs_bp, url_prefix='/logs')
    app.register_blueprint(images_bp, url_prefix='/images')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')