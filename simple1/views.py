from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

def get_state(request):
    # Example response
    data = {
        "state": "active",
        "message": "Hello from page1!"
    }
    return JsonResponse(data)
