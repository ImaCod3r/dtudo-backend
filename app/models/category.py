from peewee import CharField, BooleanField
from app.database import BaseModel

class Category(BaseModel):
    name = CharField(unique=True)
    slug = CharField(unique=True)
    is_active = BooleanField(default=True)  # Possible values: true, false

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }