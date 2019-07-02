from umongo import Document, Instance
from umongo.fields import IntField, StringField
from motor import motor_asyncio

client = motor_asyncio.AsyncIOMotorClient()
instance = Instance(client.test_db)


@instance.register
class User(Document):
    chat_id = IntField(unique=True)
    first_name = StringField()
    username = StringField()
    last_name = StringField()
