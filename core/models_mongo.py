from mongoengine import Document, StringField, ListField, DateTimeField
#from mongoengine.fields import EmailField
import datetime

class UserPlugins(Document):
    user_id = StringField(required=True)  # store Django user.id or session key
    plugins = ListField(StringField(), default=list)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'user_plugins'
    }