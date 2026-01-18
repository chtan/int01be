import importlib
import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.http import Http404


"""
#from .utils_game import get_or_create_game_state, get_page1_state, get_page2_state
#from plugins.app3.utils import get_or_create_task_state, get_page1_state, get_page2_state
app_name = "app3"  # dynamic
module_path = f"plugins.{app_name}.utils"
utils = importlib.import_module(module_path)
get_or_create_task_state = utils.get_or_create_task_state
get_page1_state = utils.get_page1_state
get_page2_state = utils.get_page2_state

#from .models_mongo import UserGameState, Page1State, Page2State
#from plugins.app3.models_mongo import UserState, Page1State, Page2State
module_path = f"plugins.{app_name}.models_mongo"
models_mongo = importlib.import_module(module_path)
UserState = models_mongo.UserState
Page1State = models_mongo.Page1State
Page2State = models_mongo.Page2State
"""


from plugins.views import plugin_dispatch


# Constants for Session Keys and URLs
#SESSION_KEY_LAST_PAGE = 'last_page'
URL_ORIGIN = '/tokentask/origin/'
#URL_PAGE_1 = '/tokentask/origin/page1/'
#URL_PAGE_2 = '/tokentask/origin/page2/'
#URL_PAGE_1 = '/plugins/app3/firstpage/'
#URL_PAGE_2 = '/plugins/app3/page2/'


def render_with_context(request, template_name, context=None, **kwargs):
    response = TemplateResponse(request, template_name, context or {}, **kwargs)
    response.render()   # make sure the template is rendered
    return response


def home(request, app_prefix):
    logger.debug(f"App prefix is {app_prefix}")

    if app_prefix not in ["mcqset1"]:
        raise Http404("App prefix not found")

    # This is needed for activate or deactivate the Review panel.
    #from plugins.mcqset1.views import MCQ_QUESTIONS
    module_path = f"plugins.{app_prefix}.views"
    views_module = importlib.import_module(module_path)
    MCQ_QUESTIONS = views_module.MCQ_QUESTIONS

    # --- Read MCQ session state ---
    mcq_answers = request.session.get('mcq_answers', {})
    total_questions = len(MCQ_QUESTIONS)
    all_answered = len(mcq_answers) == total_questions

    context = {
        'app_name': app_prefix,
        'mcq_answers': mcq_answers,
        'total_questions': total_questions,
        'all_answered': all_answered,
    }

    return render_with_context(request, "tokentask/home.html", context)


"""
@require_POST
def clear(request, app_prefix):
    logger.debug(f"App prefix is {app_prefix}")

    if app_prefix not in ["mcqset1"]:
        raise Http404("App prefix not found")

    # Clear only app-specific session keys
    #for key in list(request.session.keys()):
    #    if key.startswith(app_prefix):
    #        del request.session[key]

    # No to the above - because 1 app 1 session
    request.session.clear() # session key is preserved

    return redirect('app_home', app_prefix=app_prefix)
"""

@require_POST
def flush(request, app_prefix):
    logger.debug(f"App prefix is {app_prefix}")

    if app_prefix not in ["mcqset1"]:
        raise Http404("App prefix not found")
    
    # Delete app's db state
    #UserState.objects().delete()
    module_path = f"plugins.{app_prefix}.utils"
    utils_module = importlib.import_module(module_path)
    init_token_state = utils_module.init_token_state
    init_token_state(request)

    # This must be after the above,
    # as the session is required to access the db state.    
    request.session.flush() # session key is deleted

    return redirect('app_home', app_prefix=app_prefix)


def enter(request, app_prefix):
    logger.debug(f"App prefix is {app_prefix}")

    if app_prefix not in ["mcqset1"]:
        raise Http404("App prefix not found")

    plugin = app_prefix
    action = 'firstpage'

    return plugin_dispatch(request, plugin, action)


'''
@require_POST
def clear_session(request):
    request.session.clear()
    return redirect("origin")


@require_POST
def flush_session(request):
    request.session.flush()
    #UserGameState.objects().delete()
    UserState.objects().delete()
    return redirect("origin")

def origin_view(request):
    """
    URL: /tokentask/origin/
    """
    #request.session.clear()
    #request.session.flush()
    #print(request.session.session_key)

    #last_page = None

    #mongo_state = get_or_create_game_state(request)
    mongo_state = get_or_create_task_state(request)

    steps = mongo_state.steps
    last_page = request.session.get(SESSION_KEY_LAST_PAGE)
    print("!!!!", request.session.session_key, last_page, mongo_state.steps)

    context = {
        "last_page": last_page,
        "steps": steps,
    }
    
    # In a real app, you would render a template here.
    # For console testing, we'll just return a simple response.
    #return render(request, 'tokentask/origin.html', context)
    return render_with_context(request, "tokentask/origin.html", context)


def enter_app_view(request):
    """
    Called when the user clicks 'Enter App' from the origin page.
    Redirects to the last saved page, or page1 if it's the first time.
    """
    last_page = request.session.get(SESSION_KEY_LAST_PAGE)

    print("-------", last_page)

    if last_page:
        #return redirect(last_page)
        if '2' in last_page:
            action = 'page2'
        else:
            action = 'firstpage'
    else:
        #return redirect(URL_PAGE_1)
        request.session[SESSION_KEY_LAST_PAGE] = URL_PAGE_1
        action = 'firstpage'

    plugin = 'app3'

    return plugin_dispatch(request, plugin, action)


def page1_view(request):
    """
    URL: /tokentask/origin/page1/
    Saves the current page state and offers forward/exit.

    page1 is entered in 2 ways:
    - first entry into app
    - backward from page2
    """
    transition = request.GET.get('transition')
    mongo_state = get_or_create_game_state(request)
    steps = mongo_state.steps
    if transition == 'backward':
        steps += 1

    request.session[SESSION_KEY_LAST_PAGE] = URL_PAGE_1
    
    mongo_state.steps = steps
    mongo_state.save()

    page_state = get_page1_state(request)
    page_state.visits += 1
    page_state.save()

    context = {
        'current_page': 'Page 1',
        'forward_url': URL_PAGE_2,
        'exit_url': URL_ORIGIN,
        'steps': steps,
    }
    
    #return render(request, 'tokentask/page.html', context)
    return render_with_context(request, "tokentask/page.html", context)


def page2_view(request):
    """
    URL: /tokentask/origin/page2/
    Saves the current page state and offers backward/exit.
    """
    transition = request.GET.get('transition')
    mongo_state = get_or_create_game_state(request)
    steps = mongo_state.steps
    if transition == 'forward':
        steps += 1

    request.session[SESSION_KEY_LAST_PAGE] = URL_PAGE_2
    
    mongo_state.steps = steps
    mongo_state.save()

    page_state = get_page2_state(request)
    page_state.visits += 1
    page_state.save()

    context = {
        'current_page': 'Page 2',
        'backward_url': URL_PAGE_1,
        'exit_url': URL_ORIGIN,
        'steps': steps,
    }
    
    #return render(request, 'tokentask/page.html', context)
    return render_with_context(request, "tokentask/page.html", context)


def exit_app_view(request):
    """
    Called when the user exits the game.
    
    Possibly clearing the session state and redirects to the origin page.
    """
    # 1. Clear the last page state
    #if SESSION_KEY_LAST_PAGE in request.session:
    #    del request.session[SESSION_KEY_LAST_PAGE]
    #if SESSION_KEY_STEPS in request.session:
    #    del request.session[SESSION_KEY_STEPS]
    
    #request.session.flush() # this will even remove session key
    #request.session.clear() # this achieves the above del's but retain the session key

    return redirect(URL_ORIGIN)
'''