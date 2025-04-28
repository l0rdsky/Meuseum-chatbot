from mongoengine import Document, ReferenceField, StringField, DateTimeField, DoubleField
from models.user import User
from models.museum import Museum
import datetime

class Ticket(Document):
    user_id = ReferenceField(User, required=True, reverse_delete_rule=2)    # CASCADE
    museum_id = ReferenceField(Museum, required=True, reverse_delete_rule=2)
    ticket_type = StringField(required=True)  # e.g., "Adult", "Child"
    price = DoubleField(required=True)
    visit_date = DateTimeField(required=True)
    booking_date = DateTimeField(default=datetime.datetime.utcnow)
    status = StringField(default="booked")  # or "cancelled"
