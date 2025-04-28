from mongoengine import Document, StringField, EmailField, DateTimeField
import datetime

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    phone = StringField()
    role = StringField(default="user")  # "admin" or "user"
    created_at = DateTimeField(default=datetime.datetime.utcnow)
