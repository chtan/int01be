from django.shortcuts import render

# Create your views here.

def home_view(request):
    context = {}
    
    return render(request, 'simple6/home.html', context)


def token_view(request):
    context = {}
    
    return render(request, 'simple6/token.html', context)