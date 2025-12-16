from database import BaseModel
from peewee import ForeignKeyField, FloatField, IntegerField
from app.models.product import Product
from app.models.cart import Cart

class CartItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='items')
    product = ForeignKeyField(Product, backref='cart_items')
    quantity = IntegerField()