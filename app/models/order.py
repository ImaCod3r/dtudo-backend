from app.database import BaseModel
from peewee import CharField, ForeignKeyField, DateTimeField, FloatField
from app.models.user import User
import datetime

class Order(BaseModel):
    user = ForeignKeyField(User, backref='orders')
    total_price = FloatField()
    created_at = DateTimeField(default=datetime.datetime.now)
    address = CharField()
    phone_number = CharField(max_length=9)
    status = CharField(default='pending')  # Possible values: pending, shipped, canceled