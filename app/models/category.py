from peewee import CharField, BooleanField, ForeignKeyField
from app.database import BaseModel

class Category(BaseModel):
    name = CharField(unique=True)
    slug = CharField(unique=True)
    parent = ForeignKeyField('self', null=True, backref='children', on_delete='CASCADE')
    is_active = BooleanField(default=True)  

    def to_dict(self, include_children=True):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'parent_id': self.parent.id if self.parent else None
        }
        if include_children:
            data['children'] = [child.to_dict() for child in self.children]
        return data