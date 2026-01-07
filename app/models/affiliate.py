from peewee import CharField, ForeignKeyField, DateTimeField
from app.database import BaseModel
from app.models.user import User
import datetime
import uuid

class Affiliate(BaseModel):
    user = ForeignKeyField(User, backref='affiliate_profile', unique=True)
    bi_front = CharField() # Path or ID to image
    bi_back = CharField() # Path or ID to image
    selfie = CharField() # Path or ID to image
    status = CharField(default='pending') # pending, approved, rejected
    code = CharField(unique=True) # Unique affiliate code
    created_at = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.to_dict(),
            "bi_front": self.bi_front,
            "bi_back": self.bi_back,
            "selfie": self.selfie,
            "status": self.status,
            "code": self.code,
            "created_at": self.created_at.isoformat()
        }
