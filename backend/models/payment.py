from mongoengine import Document, ReferenceField, DoubleField, StringField, DateTimeField
from models.user import User
from models.ticket import Ticket
import datetime

class Payment(Document):
    user_id = ReferenceField(User, required=True, reverse_delete_rule=2)
    ticket_id = ReferenceField(Ticket, required=True, reverse_delete_rule=2)
    amount = DoubleField(required=True)
    payment_status = StringField(required=True)  # "paid", "pending", "failed"
    payment_method = StringField(required=True)  # "card", "upi", etc.
    transaction_id = StringField(required=True, unique=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
