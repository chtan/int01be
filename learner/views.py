from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="/core/login/")
def echo(request):
    message = request.GET.get("message", "")
    return HttpResponse(f"You said: {message}")