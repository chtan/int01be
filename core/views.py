# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Example: set a "correct" token
CORRECT_TOKENS = [
    #"MYSECRET123",
    #"MYSECRET123_3",
    "mcqset1_token1",
]
TOKEN_TO_APP_DICT = {
    #"MYSECRET123": "app1",
    #"MYSECRET123_3": "app3",
    "mcqset1_token1": "mcqset1",
}


# Redirect /core -> home or login depending on auth
def index_redirect(request):
    if request.user.is_authenticated:
        return redirect(reverse("core:home"))
    else:
        return redirect(reverse("core:login"))


# Login page
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # sets session
            return redirect(reverse("core:home"))
        else:
            error = "Invalid username or password"

    return render(request, "core/login.html", {"error": error})


@login_required(login_url="/core/login/")
def home_view(request):
    user = request.user
    is_learner = user.userprofile.is_learner
    is_coordinator = user.userprofile.is_coordinator

    breadcrumbs = [
        {"name": "Dashboard", "url": None},
    ]

    if is_learner:
        from coordinator.services import getTasksForUser
        tasks = getTasksForUser(user.username)

        context = {
            "plugins": tasks,
            "is_learner": is_learner,
            "is_coordinator": is_coordinator,
            "breadcrumbs": breadcrumbs,
        }
    elif is_coordinator:
        from coordinator.services import getTasks, getTaskStats
        usertasks = getTasks(user.username)
        taskstats = getTaskStats(user.username, usertasks)

        context = {
            "is_learner": is_learner,
            "is_coordinator": is_coordinator,
            "taskstats": taskstats,
            "breadcrumbs": breadcrumbs,
        }
    else:
        context = {
            "is_learner": is_learner,
            "is_coordinator": is_coordinator,
            "breadcrumbs": breadcrumbs,
        }
    
    return render(request, 'core/home.html', context)


def logout_view(request):
    logout(request)
    #return redirect(reverse("core:login"))
    return redirect("/")


def token_view(request):
	#context = {}

    if request.method == "POST":
        token = request.POST.get("token")
        if token in CORRECT_TOKENS:
            # Store token in session
            request.session['token_authenticated'] = True
            request.session['access_token'] = token

            # Redirect to plugin dashboard
            return redirect(f'/plugins/{TOKEN_TO_APP_DICT[token]}/firstpage')
        else:
            return render(request, "core/token.html", {"error": "Invalid token"})

    return render(request, "core/token.html")


