from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
#from .utils import get_or_create_game_state, get_page1_state, get_page2_state
from django.views.decorators.http import require_POST
#from .models_mongo import UserGameState, Page1State, Page2State



# Constants for Session Keys and URLs
SESSION_KEY_LAST_PAGE = 'last_game_page'
URL_ORIGIN = '/simple7/home/'
URL_PAGE_1 = '/simple7/home/page1/'
URL_PAGE_2 = '/simple7/home/page2/'


def render_with_context(request, template_name, context=None, **kwargs):
    response = TemplateResponse(request, template_name, context or {}, **kwargs)
    response.render()   # make sure the template is rendered
    return response


#def home_view(request):
#    context = {}
#    
#    return render(request, 'simple7/home.html', context)


def home_view(request):
    """
    URL: /simple7/home/
    """
    #request.session.clear()
    #request.session.flush()
    #print(request.session.session_key)

    #last_page = None

    #mongo_state = get_or_create_game_state(request)
    #last_page = request.session.get(SESSION_KEY_LAST_PAGE)
    #print(request.session.session_key, last_page, mongo_state.steps)

    context = {
    #    "last_page": last_page,
    }
    
    # In a real app, you would render a template here.
    # For console testing, we'll just return a simple response.
    #return render(request, 'tokentask/origin.html', context)
    return render_with_context(request, "simple7/home.html", context)



def token_view(request):
    context = {}
    
    return render(request, 'simple7/token.html', context)

