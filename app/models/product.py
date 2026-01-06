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
    public_id = CharField(unique=True, default=lambda: generate_public_id("prod"))

    def to_dict(self):
        image_url = None
        try:
            if self.image:
                image_url = self.image.url
        except (Image.DoesNotExist, AttributeError):
            image_url = None
        except Exception:
            image_url = None

        category_name = None
        try:
            if self.category:
                category_name = self.category.name
        except (Category.DoesNotExist, AttributeError):
            category_name = None
        except Exception:
            category_name = None

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': image_url,
            'category': category_name,
            'public_id': self.public_id
        }