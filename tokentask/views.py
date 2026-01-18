import importlib
import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.http import Http404

from plugins.views import plugin_dispatch


# Constants for Session Keys and URLs
#SESSION_KEY_LAST_PAGE = 'last_page'


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
