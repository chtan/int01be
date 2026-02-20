from django.shortcuts import render
from django.contrib.auth.decorators import login_required

"""
All plugins are found in the plugins app
which contains this app2 (plugin).

There are 2 types - those that are decorated with login_required
and those that are decorated with token_required.
"""

@login_required(login_url="/core/login/")
def dashboard(request):
    breadcrumbs = [
        {"name": "Dashboard", "url": "/core/home/"},
        {"name": f"Task", "url": None},  # current page
    ]

    context = {
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "app2/dashboard.html", context)
