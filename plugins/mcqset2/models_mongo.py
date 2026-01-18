from mongoengine import Document, StringField, DictField, DateTimeField
import datetime

from pathlib import Path
APP_NAME = Path(__file__).resolve().parent.name

class TaskState(Document):
    username = StringField(required=True)  # Django user.id or session key
    answers = DictField(default=dict)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': f'{APP_NAME}_task_state'
    }
