import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.http import JsonResponse
#from core.decorators import token_required
from django.contrib.auth.decorators import login_required
import markdown
from .utils import get_or_create_task_state, init_task_state, delete_task_state
from pathlib import Path
APP_NAME = Path(__file__).resolve().parent.name

TOKEN = 'access_token'
TOKEN_AUTHENTICATED_FLAG = 'token_authenticated'
SESSION_KEY_LAST_PAGE = 'last_page'
URL_HOME = f'/tokentask/{APP_NAME}/home' # tokentask hosts the landing page for token-required apps


#@token_required
#def _firstpage(request):
#    context = {
#        'APP_NAME': APP_NAME,
#    }
#    return render(request, f'{APP_NAME}/firstpage.html', context)


@login_required(login_url="/core/login/")
def clear(request):
    init_task_state(request)

    # This must be after the above,
    # as the session is required to access the db state.    
    for key in list(request.session.keys()):
        if not key.startswith("_"):
            del request.session[key]

    return redirect(request.META.get('HTTP_REFERER', '/')) # back to the same page



@login_required(login_url="/core/login/")
def exit(request):
	return redirect(URL_HOME)

#def render_with_context(request, template_name, context=None, **kwargs):
#    response = TemplateResponse(request, template_name, context or {}, **kwargs)
#    response.render()   # make sure the template is rendered
#    return response

@login_required(login_url="/core/login/")
def dashboard(request):
    logger.debug(f"App name is {APP_NAME}")
    print(f"App name is {APP_NAME}")

    #if APP_NAME not in ["mcqset1"]:
    #    raise Http404("App name not found")

    # --- Read MCQ session state ---
    mcq_answers = request.session.get('mcq_answers', {})
    total_questions = len(MCQ_QUESTIONS)
    all_answered = len(mcq_answers) == total_questions

    context = {
        'app_name': APP_NAME,
        'mcq_answers': mcq_answers,
        'total_questions': total_questions,
        'all_answered': all_answered,
    }

    #return render_with_context(request, "tokentask/home.html", context)
    return render(request, f"{APP_NAME}/dashboard.html", context)


# Define your MCQs
MCQ_QUESTIONS = [
    {
        'id': 1,
        'question': "What is the capital of France?",
        'choices': ["Paris", "London", "Berlin", "Rome"]
    },
    {
        'id': 2,
        'question': "What is 2 + 2?",
        'choices': ["3", "4", "5", "6"]
    },
    {
        'id': 3,
        'question': "Which planet is known as the Red Planet?",
        'choices': ["Earth", "Mars", "Jupiter", "Venus"]
    },
    # Add more questions as needed
]

CORRECT_ANSWERS = {
    '1': 0,  # Paris
    '2': 1,  # 4
    '3': 1,  # Mars
}

@login_required(login_url="/core/login/")
def firstpage(request):
    """
    This is accessed either via GET or POST.
    """
    # Initialize session storage for answers if not exist
    if 'mcq_answers' not in request.session:
        request.session['mcq_answers'] = {}  # {q_id: choice_index}

    # Get current question index from GET parameter, default to first
    q_index = int(request.GET.get('q', 0))
    q_index = max(0, min(q_index, len(MCQ_QUESTIONS) - 1))  # bounds check
    question = MCQ_QUESTIONS[q_index]
    q_id = question['id']

    # Handle AJAX POST for submitting an answer
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        choice_index = int(request.POST.get('choice'))
        mcq_answers = request.session['mcq_answers']
        mcq_answers[str(q_id)] = choice_index
        request.session['mcq_answers'] = mcq_answers

        # Check if all questions are answered
        all_answered = len(mcq_answers) == len(MCQ_QUESTIONS)
        return JsonResponse({'success': True, 'all_answered': all_answered})

    # Pass state to template
    mcq_answers = request.session['mcq_answers']
    all_answered = len(mcq_answers) == len(MCQ_QUESTIONS)
    selected_choice = mcq_answers.get(str(q_id))

    context = {
        'q_id': q_id,
        'question': question['question'],
        'choices': question['choices'],
        'q_index': q_index,
        'total_questions': len(MCQ_QUESTIONS),
        'selected_choice': selected_choice,
        'all_answered': all_answered,
        'app_name': APP_NAME,
    }
    return render(request, f'{APP_NAME}/firstpage.html', context)


@login_required(login_url="/core/login/")
def review(request):
    mcq_answers = request.session.get('mcq_answers', {})

    # ---- Guard: ensure all questions are answered ----
    if len(mcq_answers) != len(MCQ_QUESTIONS):
        return redirect(URL_HOME)

    # Save task state to the database
    mongo_state = get_or_create_task_state(request)
    mongo_state.answers = mcq_answers
    mongo_state.save()

    score = 0
    questions_for_review = []

    for q in MCQ_QUESTIONS:
        qid = str(q['id'])
        selected_index = mcq_answers.get(qid)
        correct_index = CORRECT_ANSWERS.get(qid)

        if selected_index == correct_index:
            score += 1

        questions_for_review.append({
            'id': q['id'],
            'app_name': APP_NAME,
            'question': q['question'],
            'choices': q['choices'],
            'selected_index': selected_index,
            'correct_index': correct_index,
            'explanation': markdown.markdown("""
**Why this is correct**

We use the quadratic formula:

$$
x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}
$$

- The discriminant is positive  
- Therefore, *two real roots* exist
""")
        })

    total_questions = len(MCQ_QUESTIONS)
    percentage = round((score / total_questions) * 100)

    context = {
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'questions': questions_for_review,
        'app_name': APP_NAME,
    }

    return render(request, f'{APP_NAME}/review.html', context)
