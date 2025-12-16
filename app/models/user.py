from peewee import CharField
from app.database import BaseModel

class User(BaseModel):
    google_id = CharField(unique=True)
    email = CharField(unique=True)
    name = CharField()
    avatar = CharField(null=True)
    role = CharField(default="customer")  # Possible roles: customer, admin
    public_id = CharField(unique=True)