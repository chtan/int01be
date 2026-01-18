from .models_mongo import TaskState


def get_or_create_task_state(request):
    try:
        username = request.user.username

        doc = TaskState.objects(username=username).first()
        if doc is None:
            doc = TaskState(username=username)
            doc.save()
        return doc
    except:
        pass


def init_task_state(request):
    try:
        username = request.user.username

        # Remove any existing state for this token
        TaskState.objects(username=username).delete()

        # Create a fresh state
        doc = TaskState(username=username)
        doc.save()

        return doc
    except:
        pass


def delete_task_state(request):
    try:
        username = request.user.username

        # Remove any existing state for this token
        TaskState.objects(username=username).delete()
    except:
        pass