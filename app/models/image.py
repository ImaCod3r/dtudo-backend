from app.database import BaseModel
from peewee import CharField, DateTimeField
from datetime import datetime

class Image(BaseModel):
    url = CharField()
    filename = CharField()
    created_at = DateTimeField(default=datetime.utcnow)