from mongoengine import *


class User(Document):
    chat_id = IntField(unique=True)
    first_name = StringField()
    username = StringField()
    last_name = StringField()
