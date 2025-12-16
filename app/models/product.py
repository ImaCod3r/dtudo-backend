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