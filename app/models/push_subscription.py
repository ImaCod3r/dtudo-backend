from peewee import ForeignKeyField, TextField
from app.database import BaseModel
from app.models.user import User

class PushSubscription(BaseModel):
    user = ForeignKeyField(User, backref='subscriptions')
    endpoint = TextField(null=False)
    p256dh = TextField(null=False)
    auth = TextField(null=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user.id,
            'endpoint': self.endpoint
        }
