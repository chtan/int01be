from .models_mongo import CoordinatorTask


def getTasks(coordinatorid):
    tasks = CoordinatorTask.objects(coordinatorid=coordinatorid)
    return [t.taskid for t in tasks]


def getTaskStats(coordinatorid, t):
    """
    Returns:
        - a dict if t is a single taskid
        - a list of dicts if t is multiple taskids
    """
    if not isinstance(t, (list, tuple, set)):
        t = [t]

    objs = CoordinatorTask.objects(
        coordinatorid=coordinatorid,
        taskid__in=list(t)
    )

    return [
        {
            "taskid": obj.taskid,
            "num_users": len(obj.userids) if obj.userids else 0
        }
        for obj in objs
    ]


def getTasksForUser(userid):
    # Query all CoordinatorTask docs where 'userid' is in the userids list
    tasks = CoordinatorTask.objects(userids=userid)
    
    # Return just the taskid values
    return [task.taskid for task in tasks]
