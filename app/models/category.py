from peewee import CharField, BooleanField
from app.database import BaseModel

class Category(BaseModel):
    name = CharField(unique=True)
    slug = CharField(unique=True)
    description = CharField(null=True)
    is_active = BooleanField(default=True)  # Possible values: true, false