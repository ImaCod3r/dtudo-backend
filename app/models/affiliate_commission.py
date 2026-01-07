from peewee import CharField, FloatField, ForeignKeyField, DateTimeField
from app.database import BaseModel
from app.models.affiliate import Affiliate
from app.models.order import Order
from app.models.orderItem import OrderItem
import datetime

class AffiliateCommission(BaseModel):
    affiliate = ForeignKeyField(Affiliate, backref='commissions')
    order = ForeignKeyField(Order, backref='affiliate_commissions')
    order_item = ForeignKeyField(OrderItem, backref='commissions')
    amount = FloatField()
    status = CharField(default='pending') # pending, available, withdrawn
    created_at = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "affiliate_id": self.affiliate.id,
            "order_public_id": self.order.public_id,
            "order_item_id": self.order_item.id,
            "amount": self.amount,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
