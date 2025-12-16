# Routes
from app.routes.products import products_bp
from app.routes.categories import categories_bp    

# Models
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.cart import Cart
from app.models.orderItem import OrderItem
from app.models.cartItem import CartItem


def config_database(db):
    db.connect()
    db.create_tables([User, Category, Product, Order, Cart, OrderItem, CartItem])

    return db

def config_routes(app):
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(categories_bp, url_prefix='/categories')