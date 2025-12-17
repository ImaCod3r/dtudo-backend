from app.database import BaseModel
from peewee import ForeignKeyField, IntegerField
from app.models.product import Product
from app.models.cart import Cart

class CartItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='items')
    product = ForeignKeyField(Product, backref='cart_items')
    quantity = IntegerField()

    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity
        }