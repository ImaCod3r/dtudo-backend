from peewee import CharField, FloatField, ForeignKeyField
from app.database import BaseModel
from app.models.category import Category

class Product(BaseModel):
    name = CharField()
    description = CharField()
    price = FloatField()
    stock = FloatField()
    image_url = CharField(null=True)
    category = ForeignKeyField(Category, backref='products', null=True)
    public_id = CharField(unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image_url': self.image_url,
            'category': self.category.name if self.category else None,
            'public_id': self.public_id
        }