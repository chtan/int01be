from .models_mongo import TokenState


def get_or_create_token_state(request):
    try:
        token = request.session['access_token']

        doc = TokenState.objects(token=token).first()
        if doc is None:
            doc = TokenState(token=token)
            doc.save()
        return doc
    except:
        pass


def init_token_state(request):
    try:
        token = request.session['access_token']

        # Remove any existing state for this token
        TokenState.objects(token=token).delete()

        # Create a fresh state
        doc = TokenState(token=token)
        doc.save()

        return doc
    except:
        pass


def delete_token_state(request):
    try:
        token = request.session['access_token']

        # Remove any existing state for this token
        TokenState.objects(token=token).delete()
    except:
        pass