from django.shortcuts import render
from mongoengine import get_db

# Create your views here.

from django.http import JsonResponse


def on_enter_get_state(request):
    collection = get_db()["simple2_col1"]
    doc = collection.find_one({})

    #data = { "steps": 0 }
    data = { "steps": doc["steps"] }
    return JsonResponse(data)


def on_exit_update_state(request):
    steps0 = request.GET.get('steps', '')
    #print("STEPS: ", steps0)
    
    collection = get_db()["simple2_col1"]
    doc = collection.find_one({})
    collection.update_one(
        {"_id": doc["_id"]},   # filter by the document's _id
        {"$inc": {"steps": 1}} # MongoDB increment operator
    )

    data = { "steps": doc["steps"] + 1 }
    #data = { "steps": 0 }
    return JsonResponse(data)
