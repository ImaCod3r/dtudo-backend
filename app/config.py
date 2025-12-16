from app.database import db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.cart import Cart
from app.models.orderItem import OrderItem
from app.models.cartItem import CartItem


def config_database():
    db.connect()
    db.create_tables([User, Category, Product, Order, Cart, OrderItem, CartItem])

    return db