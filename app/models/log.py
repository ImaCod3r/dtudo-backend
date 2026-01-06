from peewee import CharField, DateTimeField, IntegerField
from app.database import BaseModel
import datetime

class Log(BaseModel):
    log_type = CharField() # e.g., 'Success', 'Warning', 'Error'
    ip_address = CharField()
    path = CharField()
    method = CharField()
    status_code = IntegerField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.log_type,
            'ip': self.ip_address,
            'path': self.path,
            'method': self.method,
            'status_code': self.status_code,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

