from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



@login_required(login_url="/core/login/")
def echo(request):
    message = request.GET.get("message", "")
    return HttpResponse(f"You said: {message}")



@login_required(login_url="/core/login/")
def task_admin(request, taskid):
    message = request.GET.get("message", "")
    user = request.user

    return JsonResponse({
        "taskid": taskid,
        "message": message,
        "username": user.username,
    })