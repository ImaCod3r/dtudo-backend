from app.database import BaseModel
from peewee import CharField, FloatField, ForeignKeyField
from app.models.user import User

class Address(BaseModel):
    name = CharField()
    lat = FloatField()
    long = FloatField()
    user = ForeignKeyField(User, backref="addresses", null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "long": self.long,
            "user_id": self.user.public_id if self.user else None
        }