from app.database import BaseModel
from peewee import ForeignKeyField, FloatField, IntegerField, CharField
from app.models.order import Order
from app.models.product import Product

class OrderItem(BaseModel):
    order = ForeignKeyField(Order, backref='order_items')
    product = ForeignKeyField(Product, backref='items')
    quantity = IntegerField()
    price = FloatField()  # Price at the time of order
    affiliate_code = CharField(null=True)

    def to_dict(self):
        product_public_id = None
        name = "Produto não disponível"
        category = None
        image = None

        try:
            if self.product:
                product_public_id = self.product.public_id
                name = self.product.name
                category = self.product.category.name if self.product.category else None
                image = self.product.image.url if self.product.image else None
        except Exception:
            pass

        return {
            "id": self.id,
            "order_id": self.order.public_id if self.order else None,
            "product_public_id": product_public_id,
            "name": name,
            "category": category,
            "image": image,
            "quantity": self.quantity,
            "price": self.price,
            "affiliate_code": self.affiliate_code
        }