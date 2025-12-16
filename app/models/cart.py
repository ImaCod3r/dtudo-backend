from database import BaseModel
from peewee import ForeignKeyField, DateTimeField, CharField
from app.models.user import User
import datetime

class Cart(BaseModel):
    user = ForeignKeyField(User, backref='cart')
    public_id = CharField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)