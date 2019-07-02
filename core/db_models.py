from mongoengine import Document
from mongoengine.fields import IntField, StringField


class User(Document):
    chat_id = IntField(unique=True)
    first_name = StringField()
    username = StringField()
    last_name = StringField()
