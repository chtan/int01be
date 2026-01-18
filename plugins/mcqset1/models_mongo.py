from mongoengine import Document, StringField, DictField, DateTimeField
import datetime

class TokenState(Document):
    token = StringField(required=True)  # Django user.id or session key
    answers = DictField(default=dict)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'mcqset1_token_state'
    }
