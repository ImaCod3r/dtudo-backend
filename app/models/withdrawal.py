from peewee import CharField, FloatField, ForeignKeyField, DateTimeField
from app.database import BaseModel
from app.models.affiliate import Affiliate
import datetime

class Withdrawal(BaseModel):
    affiliate = ForeignKeyField(Affiliate, backref='withdrawals')
    amount = FloatField()
    iban = CharField()
    bank = CharField()
    status = CharField(default='pending') # pending, paid, rejected
    created_at = DateTimeField(default=datetime.datetime.now)
    processed_at = DateTimeField(null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "affiliate_id": self.affiliate.id,
            "amount": self.amount,
            "iban": self.iban,
            "bank": self.bank,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "processed_at": self.processed_at.isoformat() if self.processed_at else None
        }
