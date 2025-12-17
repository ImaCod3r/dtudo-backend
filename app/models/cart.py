from app.database import BaseModel
from peewee import ForeignKeyField, DateTimeField, CharField
from app.models.user import User
import datetime

class Cart(BaseModel):
    user = ForeignKeyField(User, backref='cart')
    public_id = CharField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'public_id': self.public_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }