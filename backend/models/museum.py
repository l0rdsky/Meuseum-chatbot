from mongoengine import Document, StringField, DictField

class Museum(Document):
    name = StringField(required=True)
    location = StringField(required=True)
    opening_hours = DictField(required=True)  # e.g., {"Mon-Fri": "10am-6pm"}
    ticket_prices = DictField(required=True)  # e.g., {"Adult": 100, "Child": 50}
