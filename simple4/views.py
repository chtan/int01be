from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from .utils_game import get_or_create_game_state, get_page1_state, get_page2_state

"""
session and db persistence should maintain different things.

if a value is persisted in the same way using both, then something is wrong.

in the following, we will persist steps in db
and last_page in session.

If something does wrong or browser is switched, then last_page is gone, but steps remain.
"""


# --- Constants for Session Keys and URLs ---
SESSION_KEY_LAST_PAGE = 'last_game_page' # session id; needs table in database
URL_ORIGIN = '/simple4/origin/'
URL_PAGE_1 = '/simple4/origin/page1/'
URL_PAGE_2 = '/simple4/origin/page2/'


def render_with_context(request, template_name, context=None, **kwargs):
    """
    Wrap Django's render() to return a TemplateResponse
    so context is accessible in tests.
    """
    response = TemplateResponse(request, template_name, context or {}, **kwargs)
    response.render()   # make sure the template is rendered
    return response


def origin_view(request):
    """
    URL: /simple4/origin/
    The starting point. Offers the option to enter the game.
    """
    #request.session.clear()
    #request.session.flush()
    #print(request.session.session_key)

    #last_page = None

    mongo_state = get_or_create_game_state(request)
    last_page = request.session.get(SESSION_KEY_LAST_PAGE)
    print(request.session.session_key, last_page, mongo_state.steps)

    context = {
        "last_page": last_page,
    }
    
    # In a real app, you would render a template here.
    # For console testing, we'll just return a simple response.
    #return render(request, 'simple4/origin.html', context)
    return render_with_context(request, "simple4/origin.html", context)
    

def enter_game_view(request):
    """
    Called when the user clicks 'Enter Game' from the origin page.
    Redirects to the last saved page, or page1 if it's the first time.
    """
    last_page = request.session.get(SESSION_KEY_LAST_PAGE)
    
    if last_page:
        return redirect(last_page)
    else:
        request.session[SESSION_KEY_LAST_PAGE] = URL_PAGE_1
        return redirect(URL_PAGE_1)


def page1_view(request):
    """
    URL: /simple4/origin/page1/
    Saves the current page state and offers forward/exit.

    page1 is entered in 2 ways:
    - first entry into game
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
    
    #return render(request, 'simple4/page.html', context)
    return render_with_context(request, "simple4/page.html", context)


def page2_view(request):
    """
    URL: /simple4/origin/page2/
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
    
    #return render(request, 'simple4/page.html', context)
    return render_with_context(request, "simple4/page.html", context)


def exit_game_view(request):
    """
    Called when the user exits the game.
    Clears the session state and redirects to the origin page.
    """
    # 1. Clear the last page state
    #if SESSION_KEY_LAST_PAGE in request.session:
    #    del request.session[SESSION_KEY_LAST_PAGE]
    #if SESSION_KEY_STEPS in request.session:
    #    del request.session[SESSION_KEY_STEPS]
    
    #request.session.flush() # this will even remove session key
    #request.session.clear() # this achieves the above del's but retain the session key

    return redirect(URL_ORIGIN)