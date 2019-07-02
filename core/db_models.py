from umongo import Document, MotorAsyncIOInstance
from umongo.fields import IntField, StringField

instance = MotorAsyncIOInstance()


@instance.register
class User(Document):
    chat_id = IntField(unique=True)
    first_name = StringField()
    username = StringField()
    last_name = StringField()
