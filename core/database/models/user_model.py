from umongo import Document, MotorAsyncIOInstance
from umongo.fields import IntField, StringField

instance = MotorAsyncIOInstance()


@instance.register
class User(Document):
    chat_id = IntField(unique=True)
    first_name = StringField(allow_none=True)
    username = StringField(allow_none=True)
    last_name = StringField(allow_none=True)
    locale = StringField(allow_none=True)
