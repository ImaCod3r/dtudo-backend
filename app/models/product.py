from peewee import CharField, FloatField, ForeignKeyField
from app.database import BaseModel
from app.models.category import Category
from app.models.image import Image
from app.utils.generate_public_id import generate_public_id

class Product(BaseModel):
    name = CharField()
    description = CharField()
    price = FloatField()
    image = ForeignKeyField(Image, null=True, backref="products", on_delete="SET NULL")
    category = ForeignKeyField(Category, backref='products', null=True)
    public_id = CharField(unique=True, default=generate_public_id("prod"))

    def to_dict(self):
        try:
            image_url = self.image.url if self.image else None
        except Image.DoesNotExist:
            image_url = None

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': image_url,
            'category': self.category.name if self.category else None,
            'public_id': self.public_id
        }