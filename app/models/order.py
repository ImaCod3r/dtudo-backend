from app.database import BaseModel
from peewee import CharField, IntegerField, ForeignKeyField, DateTimeField, FloatField
from app.models.user import User
from app.utils.generate_public_id import generate_public_id
import datetime

class Order(BaseModel):
    user = ForeignKeyField(User, backref='orders')
    total_price = FloatField()
    created_at = DateTimeField(default=datetime.datetime.now)
    phone_number = CharField(max_length=20, null=True)
    public_id = CharField(unique=True, default=generate_public_id("order"))
    # store address id (from Address table) when an address is created
    address_id = IntegerField(null=True)
    status = CharField(default='Pendente')  # Pendente, Confirmado, Entregue, Cancelado
    
    def to_dict(self): 
        return {
            "id": self.id, 
            "user_id": self.user.public_id,
            "total_price": self.total_price,
            "created_at": self.created_at,
            # backref from OrderItem is 'order_items'
            "items": [item.to_dict() for item in self.order_items],
            "phone_number": self.phone_number,
            "public_id": self.public_id,
            "address_id": self.address_id,
            "status": self.status
        }