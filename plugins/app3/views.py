from django.shortcuts import render, redirect
from core.decorators import token_required
from .utils import get_or_create_task_state, get_page1_state, get_page2_state
from .models_mongo import UserState, Page1State, Page2State

TOKEN = 'access_token'
TOKEN_AUTHENTICATED_FLAG = 'token_authenticated'
SESSION_KEY_LAST_PAGE = 'last_page'
URL_ORIGIN = '/core/token/'
URL_PAGE_1 = '/core/plugins.app3/firstpage/'
URL_PAGE_2 = '/core/plugins.app3/page2/'


@token_required
def firstpage(request):
    request.session[SESSION_KEY_LAST_PAGE] = URL_PAGE_1

    transition = request.GET.get('transition')
    mongo_state = get_or_create_task_state(request)
    steps = mongo_state.steps
    if transition == 'backward':
        steps += 1
    mongo_state.steps = steps
    mongo_state.save()

    page_state = get_page1_state(request)
    page_state.visits += 1
    page_state.save()

    context = {
        'current_page': 'Page 1',
        'forward_url': URL_PAGE_2,
    }
    return render(request, "app3/page.html", context)


@token_required
def page2(request):
    request.session[SESSION_KEY_LAST_PAGE] = URL_PAGE_2

    transition = request.GET.get('transition')
    mongo_state = get_or_create_task_state(request)
    steps = mongo_state.steps
    if transition == 'forward':
        steps += 1
    mongo_state.steps = steps
    mongo_state.save()

    page_state = get_page2_state(request)
    page_state.visits += 1
    page_state.save()

    context = {
        'current_page': 'Page 2',
        'backward_url': URL_PAGE_1,
    }
    return render(request, "app3/page.html", context)


@token_required
def exit(request):
    return redirect(URL_ORIGIN)
