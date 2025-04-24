from django.shortcuts import render
from django.http import JsonResponse
from .gemini_chat import get_gemini_response


# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Money Parse'
    return render(request, 'home/index.html', {
        'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})

def profile(request):
    return render(request, 'home/profile.html')

def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "")
        response = get_gemini_response(user_input, request.user)
        return JsonResponse({"response": response})
    return render(request, "home/chatbot.html")