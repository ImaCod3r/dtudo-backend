from database import BaseModel
from peewee import ForeignKeyField, FloatField, IntegerField
from app.models.order import Order
from app.models.product import Product

class OrderItem(BaseModel):
    order = ForeignKeyField(Order, backref='order_items')
    product = ForeignKeyField(Product, backref='items')
    quantity = IntegerField()
    price = FloatField()  # Price at the time of order