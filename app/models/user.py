from peewee import CharField
from app.database import BaseModel

class User(BaseModel):
    google_id = CharField(unique=True)
    email = CharField(unique=True)
    name = CharField()
    avatar = CharField(null=True)
    role = CharField(default="customer")  # Possible roles: customer, admin
    public_id = CharField(unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'google_id': self.google_id,
            'email': self.email,
            'name': self.name,
            'avatar': self.avatar,
            'role': self.role,
            'public_id': self.public_id
        }