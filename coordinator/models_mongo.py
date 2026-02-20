from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    DateTimeField
)
import datetime


class CoordinatorTask(Document):
    coordinatorid = StringField(required=True)
    taskid = StringField(required=True, unique=True)  # only this is unique now
    userids = ListField(StringField(), default=list)
    is_active = BooleanField(default=True)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'coordinator_task'
    }
