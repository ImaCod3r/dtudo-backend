from peewee import CharField
from app.database import BaseModel
from app.utils.generate_public_id import generate_public_id

class User(BaseModel):
    google_id = CharField(unique=True)
    email = CharField(unique=True)
    name = CharField()
    avatar = CharField(null=True) 
    public_id = CharField(null=False, unique=True, default=generate_public_id("user"))
    role = CharField(default="customer") # customer ou admin
    phone = CharField(unique=True, null=True)


    def to_dict(self):
        return {
            'id': self.id,
            'google_id': self.google_id,
            'email': self.email,
            'name': self.name,
            'avatar': self.avatar,
            'public_id': self.public_id,
            'role': self.role,
            'phone': self.phone
        }