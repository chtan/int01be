from mongoengine import Document, StringField, IntField, DateTimeField
from mongoengine.fields import EmailField
import datetime

class UserGameState(Document):
    user_id = StringField(required=True)  # store Django user.id or session key
    steps = IntField(default=0)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'simple5_user_game_state'
    }

class Page1State(Document):
    # This should be replaced by the owner of the game.
    #user_id = StringField(required=True)  # store Django user.id or session key
    
    visits = IntField(default=0)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'simple5_page1_state'
    }


class Page2State(Document):
    # This should be replaced by the owner of the game.
    #user_id = StringField(required=True)  # store Django user.id or session key
    
    visits = IntField(default=0)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'simple5_page2_state'
    }
