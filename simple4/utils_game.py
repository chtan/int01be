from .models_mongo import UserGameState, Page1State, Page2State

"""
session vs db persistence:

* **Session** = browser RAM
* **MongoDB** = hard disk



Understanding session key:

If the browser already has a cookie (called sessionid), Django reads it:
session_key becomes the string from the cookie.

If the browser does not have a cookie (first visit):
request.session.session_key is None.

When you first write something to the session (or explicitly call request.session.save()), Django:

Generates a new session key, e.g., '9c4f1a2b...'.
Stores an empty session row in the session backend.
Sends a Set-Cookie header back to the browser:
Set-Cookie: sessionid=9c4f1a2b...; Path=/; HttpOnly

After this, request.session.session_key is a string, even before the response reaches the browser.



Clearing db:
int01be_development> db.user_game_state.deleteMany({})
{ acknowledged: true, deletedCount: 1 }
int01be_development> db.user_game_state.find({})



Clearing session:

| Use case                          | Method                           |
| --------------------------------- | -------------------------------- |
| Clear all data for current user   | `request.session.flush()`        |
| Remove specific key               | `del request.session['key']`     |
| Keep session but clear data       | `request.session.clear()`        |
| Clear expired sessions            | `python manage.py clearsessions` |
| Clear all sessions (force logout) | delete all session objects in DB |


request.session.clear()
Clears all data stored in the session dictionary, but keeps the same session key.


request.session.flush()
Deletes the entire session from the backend (DB, cache, etc.) (including session key).

python manage.py clearsessions
clean up expired session records in the session backend

"""

def get_user_key(request):
    """
    Use Django user if logged in; else use session key.
    
    Since authentication is not set up:
    - request.user == AnonymousUser()
    - request.user.is_authenticated == False
    """

    # Print for debugging
    #print(request.user.is_authenticated, request.session.session_key)

    if request.user.is_authenticated:
        return str(request.user.id)

    # Ensure session exists and get session key
    if not request.session.session_key:
        request.session.save()  # creates the session and cookie
    return request.session.session_key  # now guaranteed to be non-None


def get_or_create_game_state(request):
    """
    Returns a MongoEngine document for this user/session,
    creating one if it doesn't exist.
    """
    user_key = get_user_key(request)

    doc = UserGameState.objects(user_id=user_key).first()
    if doc is None:
        doc = UserGameState(user_id=user_key)
        doc.save()
    return doc


def get_page1_state(request):
    """
    Returns a MongoEngine document for this user/session,
    creating one if it doesn't exist.
    """
    doc = Page1State.objects().first()
    if doc is None:
        doc = Page1State()
        doc.save()
    return doc


def get_page2_state(request):
    """
    Returns a MongoEngine document for this user/session,
    creating one if it doesn't exist.
    """
    doc = Page2State.objects().first()
    if doc is None:
        doc = Page2State()
        doc.save()
    return doc
