from database import BaseModel
from peewee import ForeignKeyField, DateTimeField
from app.models.user import User
import datetime

class Cart(BaseModel):
    user = ForeignKeyField(User, backref='cart')
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)