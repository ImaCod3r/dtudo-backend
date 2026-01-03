from app.database import BaseModel
from peewee import ForeignKeyField, FloatField, IntegerField
from app.models.order import Order
from app.models.product import Product

class OrderItem(BaseModel):
    order = ForeignKeyField(Order, backref='order_items')
    product = ForeignKeyField(Product, backref='items')
    quantity = IntegerField()
    price = FloatField()  # Price at the time of order

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order.public_id,
            "product_public_id": self.product.public_id,
            "name": self.product.name,
            "category": self.product.category.name if self.product.category else None,
            "image": self.product.image.url if self.product.image else None,
            "quantity": self.quantity,
            "price": self.price
        }