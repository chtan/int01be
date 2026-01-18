from django.shortcuts import render, redirect
from django.http import JsonResponse
from core.decorators import token_required
import markdown
from .utils import get_or_create_token_state
from pathlib import Path
app_name = Path(__file__).resolve().parent.name

TOKEN = 'access_token'
TOKEN_AUTHENTICATED_FLAG = 'token_authenticated'
SESSION_KEY_LAST_PAGE = 'last_page'
URL_HOME = f'/tokentask/{app_name}/home' # tokentask hosts the landing page for token-required apps


#@token_required
#def _firstpage(request):
#    context = {
#        'app_name': app_name,
#    }
#    return render(request, f'{app_name}/firstpage.html', context)


@token_required
def exit(request):
	return redirect(URL_HOME)




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

@token_required
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
        'all_answered': all_answered
    }
    return render(request, 'mcqset1/firstpage.html', context)


@token_required
def review(request):
    mcq_answers = request.session.get('mcq_answers', {})

    # ---- Guard: ensure all questions are answered ----
    if len(mcq_answers) != len(MCQ_QUESTIONS):
        return redirect(URL_HOME)

    # Save token state to the database
    mongo_state = get_or_create_token_state(request)
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
        'questions': questions_for_review
    }

    return render(request, 'mcqset1/review.html', context)
